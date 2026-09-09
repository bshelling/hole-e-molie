"""Browser management for web automation with Playwright"""

from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from pathlib import Path
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class BrowserManager:
    """
    Manages Playwright browser context with session persistence

    Usage:
        async with BrowserManager() as context:
            page = await context.new_page()
            await page.goto("https://example.com")
    """

    def __init__(
        self,
        headless: bool = True,
        session_file: Optional[str] = None,
        viewport: Optional[dict] = None,
        slow_mo: int = 0
    ):
        """
        Initialize browser manager

        Args:
            headless: Run browser in headless mode (default: True)
            session_file: Path to save/load session state (cookies, etc.)
            viewport: Browser viewport size (default: 1280x720)
            slow_mo: Slow down operations by N milliseconds (for debugging)
        """
        self.headless = headless
        self.session_file = session_file or "/Users/shelling/Projects/holeemoly/agents/nola311_session.json"
        self.viewport = viewport or {'width': 1280, 'height': 720}
        self.slow_mo = slow_mo

        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None

        logger.info(
            f"BrowserManager initialized: headless={headless}, "
            f"session_file={self.session_file}, viewport={self.viewport}"
        )

    async def __aenter__(self) -> BrowserContext:
        """
        Async context manager entry - starts browser and creates context

        Returns:
            BrowserContext ready for use
        """
        logger.info("Starting Playwright browser...")

        # Start Playwright
        self.playwright = await async_playwright().start()

        # Launch browser
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled'  # Avoid detection
            ],
            slow_mo=self.slow_mo
        )

        logger.info(f"Browser launched (headless={self.headless})")

        # Check if session file exists
        session_path = Path(self.session_file)
        storage_state = None

        if session_path.exists():
            logger.info(f"Loading session from {self.session_file}")
            storage_state = self.session_file
        else:
            logger.info("No existing session found, starting fresh")

        # Create context with session state
        self.context = await self.browser.new_context(
            storage_state=storage_state,
            viewport=self.viewport,
            user_agent=(
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            # Additional context options
            accept_downloads=True,
            has_touch=False,
            is_mobile=False,
            locale='en-US',
            timezone_id='America/Chicago',  # New Orleans timezone
        )

        logger.info("Browser context created")

        return self.context

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit - saves session and closes browser

        Saves session state (cookies, localStorage) before closing.
        """
        logger.info("Closing browser...")

        # Save session state
        if self.context:
            try:
                await self.context.storage_state(path=self.session_file)
                logger.info(f"Session saved to {self.session_file}")
            except Exception as e:
                logger.warning(f"Failed to save session: {e}")

        # Close browser
        if self.context:
            await self.context.close()

        if self.browser:
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()

        logger.info("Browser closed")

    async def clear_session(self):
        """Clear saved session state"""
        session_path = Path(self.session_file)
        if session_path.exists():
            session_path.unlink()
            logger.info(f"Session cleared: {self.session_file}")
        else:
            logger.info("No session to clear")


async def create_page(context: BrowserContext) -> Page:
    """
    Helper to create a new page with common settings

    Args:
        context: Browser context from BrowserManager

    Returns:
        Configured Page instance
    """
    page = await context.new_page()

    # Set default timeout
    page.set_default_timeout(30000)  # 30 seconds

    # Set default navigation timeout
    page.set_default_navigation_timeout(30000)

    return page
