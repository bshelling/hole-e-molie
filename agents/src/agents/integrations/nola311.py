"""NOLA-311 QuickBase integration for pothole reporting"""

from agents.integrations.browser import BrowserManager, create_page
from agents.models import PotholeReport, StatusResult, SubmissionResult
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout
from datetime import datetime
import logging
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

# NOLA-311 URLs
NOLA311_FORM_URL = "https://opcd.quickbase.com/nav/app/bn79jh4a4/table/bn8jze2s7/action/nwr?nexturl=%2Fdb%2Fbn79jh4a4%3Fa%3Dshowpage%26pageIdV2%3Dquickbase.com-DashboardGroup-9e8df6e8-4d3f-4dc9-918f-ce43c863dfda&page=3"
NOLA311_STATUS_URL = "https://opcd.quickbase.com/status"  # TBD - needs reconnaissance

# Form field selectors - TO BE UPDATED AFTER FORM RECONNAISSANCE
# These are placeholder selectors that need to be determined by running
# scripts/explore_nola311.py and analyzing the form structure
FORM_SELECTORS = {
    # Location fields
    'address': 'input[name="address"]',  # TBD
    'cross_street': 'input[name="cross_street"]',  # TBD
    'landmark': 'input[name="landmark"]',  # TBD

    # Issue details
    'description': 'textarea[name="description"]',  # TBD
    'issue_type': 'select[name="issue_type"]',  # TBD
    'severity': 'select[name="severity"]',  # TBD

    # Reporter info
    'reporter_name': 'input[name="name"]',  # TBD
    'email': 'input[name="email"]',  # TBD
    'phone': 'input[name="phone"]',  # TBD

    # Submission
    'submit_button': 'button[type="submit"]',  # TBD

    # Confirmation
    'confirmation_message': '.confirmation',  # TBD
    'reference_number': '.reference-number',  # TBD
}


class NOLA311Connector:
    """
    Connector for NOLA-311 QuickBase form submission and status checking

    NOTE: Form selectors need to be updated after running form reconnaissance.
    Run: uv run python scripts/explore_nola311.py
    Then update FORM_SELECTORS above with actual field names/IDs.
    """

    def __init__(self, headless: bool = True, screenshot_dir: str = None):
        """
        Initialize NOLA-311 connector

        Args:
            headless: Run browser in headless mode
            screenshot_dir: Directory to save error screenshots
        """
        self.headless = headless
        self.screenshot_dir = screenshot_dir or "/Users/shelling/Projects/holeemoly/agents/docs/screenshots"

        # Create screenshot directory if it doesn't exist
        Path(self.screenshot_dir).mkdir(parents=True, exist_ok=True)

        logger.info(f"NOLA311Connector initialized: headless={headless}")

    async def submit_report(
        self,
        report: PotholeReport,
        max_retries: int = 3
    ) -> SubmissionResult:
        """
        Submit pothole report to NOLA-311

        Args:
            report: PotholeReport with all required information
            max_retries: Maximum number of retry attempts

        Returns:
            SubmissionResult with success status and reference number
        """
        logger.info(f"Submitting report for {report.location.address}")

        for attempt in range(max_retries):
            try:
                async with BrowserManager(headless=self.headless) as context:
                    page = await create_page(context)

                    # Navigate to form
                    logger.info(f"Navigating to form (attempt {attempt + 1}/{max_retries})")
                    await page.goto(NOLA311_FORM_URL, wait_until='networkidle', timeout=30000)

                    # Wait for form to be ready
                    await asyncio.sleep(2)

                    # Fill form fields
                    await self._fill_form(page, report)

                    # Submit form
                    reference_number = await self._submit_form(page)

                    logger.info(f"✓ Report submitted successfully: {reference_number}")

                    return SubmissionResult(
                        success=True,
                        reference_number=reference_number,
                        submitted_at=datetime.utcnow()
                    )

            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {e}")

                # Save screenshot on error
                if attempt == max_retries - 1:
                    try:
                        screenshot_path = f"{self.screenshot_dir}/error_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
                        await page.screenshot(path=screenshot_path, full_page=True)
                        logger.info(f"Error screenshot saved: {screenshot_path}")
                    except:
                        pass

                # Exponential backoff
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 1s, 2s, 4s
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    # Final attempt failed
                    return SubmissionResult(
                        success=False,
                        error_message=str(e),
                        submitted_at=datetime.utcnow()
                    )

        # Should not reach here
        return SubmissionResult(
            success=False,
            error_message="Max retries exceeded",
            submitted_at=datetime.utcnow()
        )

    async def _fill_form(self, page: Page, report: PotholeReport) -> None:
        """
        Fill out the pothole report form

        Args:
            page: Playwright page object
            report: PotholeReport data to fill
        """
        logger.info("Filling form fields...")

        try:
            # Location fields
            if FORM_SELECTORS['address']:
                await page.fill(FORM_SELECTORS['address'], report.location.address)
                logger.debug(f"Filled address: {report.location.address}")

            if report.location.cross_street and FORM_SELECTORS['cross_street']:
                await page.fill(FORM_SELECTORS['cross_street'], report.location.cross_street)

            if report.location.landmark and FORM_SELECTORS['landmark']:
                await page.fill(FORM_SELECTORS['landmark'], report.location.landmark)

            # Description
            if FORM_SELECTORS['description']:
                await page.fill(FORM_SELECTORS['description'], report.description)
                logger.debug(f"Filled description: {report.description[:50]}...")

            # Issue type dropdown (select "Pothole")
            if FORM_SELECTORS['issue_type']:
                await page.select_option(FORM_SELECTORS['issue_type'], label='Pothole')

            # Severity (if field exists)
            if FORM_SELECTORS['severity']:
                severity_map = {'low': 'Low', 'medium': 'Medium', 'high': 'High'}
                await page.select_option(
                    FORM_SELECTORS['severity'],
                    label=severity_map[report.severity]
                )

            # Reporter information
            if FORM_SELECTORS['reporter_name']:
                await page.fill(FORM_SELECTORS['reporter_name'], report.reporter_name)

            if FORM_SELECTORS['email']:
                await page.fill(FORM_SELECTORS['email'], report.email)

            if report.phone and FORM_SELECTORS['phone']:
                await page.fill(FORM_SELECTORS['phone'], report.phone)

            logger.info("✓ Form filled successfully")

        except Exception as e:
            logger.error(f"Error filling form: {e}")
            raise

    async def _submit_form(self, page: Page) -> str:
        """
        Submit the form and extract reference number

        Args:
            page: Playwright page object

        Returns:
            Reference number from NOLA-311
        """
        logger.info("Submitting form...")

        try:
            # Click submit button
            if FORM_SELECTORS['submit_button']:
                await page.click(FORM_SELECTORS['submit_button'])
                logger.debug("Submit button clicked")

            # Wait for confirmation (adjust selector based on actual form behavior)
            await page.wait_for_selector(
                FORM_SELECTORS['confirmation_message'],
                timeout=10000
            )

            # Extract reference number
            reference_element = await page.query_selector(FORM_SELECTORS['reference_number'])
            if reference_element:
                reference_number = await reference_element.inner_text()
                reference_number = reference_number.strip()
                logger.info(f"✓ Reference number: {reference_number}")
                return reference_number
            else:
                raise Exception("Could not find reference number on confirmation page")

        except PlaywrightTimeout:
            logger.error("Timeout waiting for confirmation page")
            raise Exception("Form submission timeout - confirmation page did not load")

        except Exception as e:
            logger.error(f"Error during form submission: {e}")
            raise

    async def check_status(
        self,
        reference_number: str,
        max_retries: int = 3
    ) -> StatusResult:
        """
        Check status of existing NOLA-311 report

        Args:
            reference_number: NOLA-311 reference number
            max_retries: Maximum retry attempts

        Returns:
            StatusResult with current status
        """
        logger.info(f"Checking status for: {reference_number}")

        for attempt in range(max_retries):
            try:
                async with BrowserManager(headless=self.headless) as context:
                    page = await create_page(context)

                    # Navigate to status page
                    # TODO: Determine actual status lookup method after reconnaissance
                    # Options: URL parameter, search form, separate page, etc.
                    status_url = f"{NOLA311_STATUS_URL}?ref={reference_number}"
                    await page.goto(status_url, wait_until='networkidle', timeout=30000)

                    # Parse status information
                    status_info = await self._parse_status_page(page)

                    # Normalize status
                    normalized_status = self._normalize_status(status_info['raw_status'])

                    logger.info(f"✓ Status: {normalized_status} ({status_info['raw_status']})")

                    return StatusResult(
                        reference_number=reference_number,
                        status=normalized_status,
                        raw_status=status_info['raw_status'],
                        notes=status_info['notes'],
                        updated_at=datetime.utcnow()
                    )

            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{max_retries} failed: {e}")

                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                else:
                    # Return unknown status on failure
                    return StatusResult(
                        reference_number=reference_number,
                        status='unknown',
                        raw_status='Error',
                        notes=f"Failed to check status: {str(e)}",
                        updated_at=datetime.utcnow()
                    )

    async def _parse_status_page(self, page: Page) -> dict:
        """
        Parse status information from status page

        Args:
            page: Playwright page object

        Returns:
            Dict with raw_status and notes
        """
        # TODO: Update selectors after form reconnaissance
        # These are placeholders

        try:
            # Extract status text
            status_selector = '.status-field'  # TBD
            status_element = await page.query_selector(status_selector)
            raw_status = await status_element.inner_text() if status_element else 'Unknown'

            # Extract notes/updates
            notes_selector = '.status-notes'  # TBD
            notes_element = await page.query_selector(notes_selector)
            notes = await notes_element.inner_text() if notes_element else ''

            return {
                'raw_status': raw_status.strip(),
                'notes': notes.strip()
            }

        except Exception as e:
            logger.error(f"Error parsing status page: {e}")
            return {
                'raw_status': 'Unknown',
                'notes': f'Parse error: {str(e)}'
            }

    def _normalize_status(self, raw_status: str) -> str:
        """
        Normalize NOLA-311 status to internal status

        Args:
            raw_status: Status string from NOLA-311

        Returns:
            Normalized status: submitted, in_progress, resolved, duplicate, closed, unknown
        """
        # Status mapping based on expected NOLA-311 status values
        # Update after actual status values are discovered
        status_map = {
            'open': 'submitted',
            'new': 'submitted',
            'submitted': 'submitted',
            'in progress': 'in_progress',
            'assigned': 'in_progress',
            'working': 'in_progress',
            'closed': 'resolved',
            'completed': 'resolved',
            'resolved': 'resolved',
            'fixed': 'resolved',
            'duplicate': 'duplicate',
            'cancelled': 'closed',
            'canceled': 'closed',
        }

        normalized = raw_status.lower().strip()
        return status_map.get(normalized, 'unknown')
