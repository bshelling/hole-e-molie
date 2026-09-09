"""
Interactive script to explore NOLA-311 QuickBase form structure

This script uses Playwright in headed mode to navigate to the NOLA-311
form and analyze its structure for automation purposes.

Usage:
    uv run python scripts/explore_nola311.py
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime


NOLA311_FORM_URL = "https://opcd.quickbase.com/nav/app/bn79jh4a4/table/bn8jze2s7/action/nwr?nexturl=%2Fdb%2Fbn79jh4a4%3Fa%3Dshowpage%26pageIdV2%3Dquickbase.com-DashboardGroup-9e8df6e8-4d3f-4dc9-918f-ce43c863dfda&page=3"


async def explore_form():
    """Explore the NOLA-311 QuickBase form"""

    print("=" * 80)
    print("NOLA-311 Form Reconnaissance")
    print("=" * 80)
    print()
    print(f"Form URL: {NOLA311_FORM_URL}")
    print()
    print("Starting Playwright in headed mode...")
    print("This will open a browser window for manual exploration.")
    print()

    async with async_playwright() as p:
        # Launch browser in headed mode to see what's happening
        browser = await p.chromium.launch(
            headless=False,  # Show browser window
            slow_mo=1000      # Slow down by 1 second for visibility
        )

        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )

        page = await context.new_page()

        print("Navigating to form...")
        try:
            await page.goto(NOLA311_FORM_URL, wait_until='networkidle', timeout=30000)
            print("✓ Page loaded successfully")
            print()
        except Exception as e:
            print(f"✗ Error loading page: {e}")
            await browser.close()
            return

        # Wait a moment for page to stabilize
        await asyncio.sleep(2)

        print("Analyzing form structure...")
        print("-" * 80)
        print()

        # Find all input fields
        try:
            inputs = await page.query_selector_all('input')
            print(f"Found {len(inputs)} input fields:")
            print()

            for i, input_elem in enumerate(inputs, 1):
                input_type = await input_elem.get_attribute('type') or 'text'
                input_name = await input_elem.get_attribute('name') or 'N/A'
                input_id = await input_elem.get_attribute('id') or 'N/A'
                input_placeholder = await input_elem.get_attribute('placeholder') or 'N/A'
                is_required = await input_elem.get_attribute('required')

                print(f"  Input #{i}:")
                print(f"    Type: {input_type}")
                print(f"    Name: {input_name}")
                print(f"    ID: {input_id}")
                print(f"    Placeholder: {input_placeholder}")
                print(f"    Required: {'Yes' if is_required else 'No'}")
                print()

        except Exception as e:
            print(f"Error analyzing inputs: {e}")

        # Find all textareas
        try:
            textareas = await page.query_selector_all('textarea')
            print(f"Found {len(textareas)} textarea fields:")
            print()

            for i, textarea in enumerate(textareas, 1):
                textarea_name = await textarea.get_attribute('name') or 'N/A'
                textarea_id = await textarea.get_attribute('id') or 'N/A'
                textarea_placeholder = await textarea.get_attribute('placeholder') or 'N/A'
                is_required = await textarea.get_attribute('required')

                print(f"  Textarea #{i}:")
                print(f"    Name: {textarea_name}")
                print(f"    ID: {textarea_id}")
                print(f"    Placeholder: {textarea_placeholder}")
                print(f"    Required: {'Yes' if is_required else 'No'}")
                print()

        except Exception as e:
            print(f"Error analyzing textareas: {e}")

        # Find all select dropdowns
        try:
            selects = await page.query_selector_all('select')
            print(f"Found {len(selects)} select dropdowns:")
            print()

            for i, select in enumerate(selects, 1):
                select_name = await select.get_attribute('name') or 'N/A'
                select_id = await select.get_attribute('id') or 'N/A'
                is_required = await select.get_attribute('required')

                # Get options
                options = await select.query_selector_all('option')
                option_values = []
                for opt in options:
                    value = await opt.get_attribute('value')
                    text = await opt.inner_text()
                    option_values.append(f"{text} (value={value})")

                print(f"  Select #{i}:")
                print(f"    Name: {select_name}")
                print(f"    ID: {select_id}")
                print(f"    Required: {'Yes' if is_required else 'No'}")
                print(f"    Options: {len(options)}")
                for opt in option_values[:5]:  # Show first 5 options
                    print(f"      - {opt}")
                if len(option_values) > 5:
                    print(f"      ... and {len(option_values) - 5} more")
                print()

        except Exception as e:
            print(f"Error analyzing selects: {e}")

        # Find buttons
        try:
            buttons = await page.query_selector_all('button, input[type="submit"]')
            print(f"Found {len(buttons)} buttons:")
            print()

            for i, button in enumerate(buttons, 1):
                button_type = await button.get_attribute('type') or 'button'
                button_text = await button.inner_text() if button else ''
                button_value = await button.get_attribute('value') or 'N/A'

                print(f"  Button #{i}:")
                print(f"    Type: {button_type}")
                print(f"    Text: {button_text}")
                print(f"    Value: {button_value}")
                print()

        except Exception as e:
            print(f"Error analyzing buttons: {e}")

        print("-" * 80)
        print()
        print("Manual Exploration:")
        print("  - Browser window is open for manual form inspection")
        print("  - Try filling out the form manually to understand the flow")
        print("  - Check Network tab in DevTools for POST requests")
        print("  - Note any hidden fields or CSRF tokens")
        print()
        print("Press Enter when done exploring (this will close the browser)...")

        # Keep browser open for manual exploration
        input()

        print()
        print("Saving page HTML for offline analysis...")
        html_content = await page.content()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_file = f"/Users/shelling/Projects/holeemoly/agents/docs/nola311_form_{timestamp}.html"

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✓ HTML saved to: {html_file}")

        # Take a screenshot
        screenshot_file = f"/Users/shelling/Projects/holeemoly/agents/docs/nola311_form_{timestamp}.png"
        await page.screenshot(path=screenshot_file, full_page=True)
        print(f"✓ Screenshot saved to: {screenshot_file}")

        print()
        print("Closing browser...")
        await browser.close()

        print()
        print("=" * 80)
        print("Reconnaissance Complete")
        print("=" * 80)
        print()
        print("Next steps:")
        print("  1. Review the HTML file and screenshot")
        print("  2. Document findings in docs/nola311_form_spec.md")
        print("  3. Implement form automation based on findings")
        print()


if __name__ == "__main__":
    asyncio.run(explore_form())
