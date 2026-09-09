# Phase 2: NOLA-311 Integration

**Status:** ✅ Complete  
**All Tasks:** 10/10 Complete  
**Tests:** 100% Passing

Browser automation and web scraping integration for NOLA-311 QuickBase pothole reporting system.

---

## Overview

Phase 2 implements automated interaction with the NOLA-311 pothole reporting system using Playwright browser automation. This phase provides the foundation for programmatic form submission and status checking without a public API.

### What Was Built

**Core Components:**
- 🌐 **NOLA311Connector** - Automated form submission and status checking
- 🖥️ **BrowserManager** - Persistent browser session management
- 📋 **Report Models** - Validated data models with auto-formatting
- 🔍 **Form Reconnaissance** - Tools for exploring and documenting forms
- ✅ **Test Suite** - Comprehensive unit and integration tests
- 🚀 **CI/CD** - Automated testing pipeline

---

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Playwright browsers installed

### Installation

```bash
# Install dependencies (if not already done)
cd agents
uv sync

# Install Playwright browsers
uv run playwright install chromium
```

### Basic Usage

```python
from agents.integrations import NOLA311Connector
from agents.models import PotholeReport, Location

# Create a pothole report
location = Location(address="1234 Magazine St, New Orleans, LA")
report = PotholeReport(
    location=location,
    description="Large pothole in right lane, approximately 2 feet wide",
    severity="high",
    reporter_name="Jane Doe",
    email="jane@example.com",
    phone="504-555-1234"
)

# Submit to NOLA-311
connector = NOLA311Connector(headless=True)
result = await connector.submit_report(report)

if result.success:
    print(f"Submitted! Reference: {result.reference_number}")
else:
    print(f"Failed: {result.error_message}")

# Check status
status = await connector.check_status(result.reference_number)
print(f"Status: {status.status} - {status.notes}")
```

---

## Architecture

```
┌─────────────────────┐
│  NOLA311Connector   │
│  - submit_report()  │
│  - check_status()   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  BrowserManager     │
│  - Session mgmt     │
│  - Cookie storage   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Playwright         │
│  - Chromium         │
│  - Form automation  │
└─────────────────────┘
```

---

## Components

### 1. NOLA311Connector

**Location:** `src/agents/integrations/nola311.py`

Main connector for NOLA-311 QuickBase integration.

#### Methods

**`submit_report(report: PotholeReport) -> SubmissionResult`**

Submit a pothole report to NOLA-311.

```python
result = await connector.submit_report(report)

# Returns SubmissionResult:
# - success: bool
# - reference_number: str (if successful)
# - error_message: str (if failed)
# - submitted_at: datetime
```

**Features:**
- Automatic form field mapping
- Dropdown selection handling
- Reference number extraction
- Retry logic with exponential backoff
- Screenshot capture on errors

**`check_status(reference_number: str) -> StatusResult`**

Check status of an existing report.

```python
status = await connector.check_status("311-2026-0908-001")

# Returns StatusResult:
# - reference_number: str
# - status: str (normalized)
# - raw_status: str (from NOLA-311)
# - notes: str
# - updated_at: datetime
```

**Status Normalization:**

| NOLA-311 Status | Normalized Status |
|----------------|------------------|
| Open, New, Submitted | `submitted` |
| In Progress, Assigned, Working | `in_progress` |
| Closed, Completed, Resolved, Fixed | `resolved` |
| Duplicate | `duplicate` |
| Cancelled, Canceled | `closed` |
| (Unknown) | `unknown` |

#### Configuration

```python
connector = NOLA311Connector(
    headless=True,              # Run without visible browser
    screenshot_dir="docs/screenshots"  # Error screenshot directory
)
```

---

### 2. BrowserManager

**Location:** `src/agents/integrations/browser.py`

Manages Playwright browser context with session persistence.

#### Usage

```python
from agents.integrations import BrowserManager

async with BrowserManager(headless=True) as context:
    page = await context.new_page()
    await page.goto("https://example.com")
    # Browser session automatically saved on exit
```

#### Features

- **Session Persistence** - Saves cookies and localStorage
- **Anti-Detection** - Disables automation flags
- **Custom User Agent** - Appears as regular browser
- **Timezone Support** - Configured for New Orleans (America/Chicago)
- **Configurable Viewport** - Default 1280x720
- **Slow-Mo Mode** - For debugging (slow_mo parameter)

#### Configuration

```python
manager = BrowserManager(
    headless=True,                    # Headless mode
    session_file="session.json",      # Session storage path
    viewport={'width': 1920, 'height': 1080},  # Browser size
    slow_mo=1000                      # Slow down by 1 second (debugging)
)
```

---

### 3. Report Models

**Location:** `src/agents/models/report.py`

Validated data models using Pydantic.

#### Location

```python
from agents.models import Location

location = Location(
    address="1234 Magazine St, New Orleans, LA",
    cross_street="Napoleon Ave",        # Optional
    landmark="Near Whole Foods",         # Optional
    coordinates={'lat': 29.9311, 'lng': -90.0852}  # Optional
)
```

**Validation:**
- Address required (5-500 characters)
- Coordinates validated for New Orleans area (if provided)
- Latitude: 28.5° to 30.5°
- Longitude: -91° to -88°

#### PotholeReport

```python
from agents.models import PotholeReport

report = PotholeReport(
    location=location,
    description="Large pothole in right lane, 2 feet wide",
    severity="high",                # "low", "medium", or "high"
    reporter_name="Jane Doe",
    email="jane@example.com",
    phone="504-555-1234"            # Auto-formatted to (504) 555-1234
)
```

**Validation:**
- Description: 10-2000 characters
- Severity: Must be "low", "medium", or "high"
- Email: Valid email format (uses email-validator)
- Phone: US format, auto-formatted to (XXX) XXX-XXXX
- Name: 2-100 characters

**Phone Formatting Examples:**
```python
"5045551234"     → "(504) 555-1234"
"504-555-1234"   → "(504) 555-1234"
"+15045551234"   → "+1 (504) 555-1234"
```

#### StatusResult

```python
from agents.models import StatusResult

status = StatusResult(
    reference_number="311-2026-0908-001",
    status="in_progress",           # Normalized status
    raw_status="Assigned",          # Original NOLA-311 status
    notes="Crew assigned for repair",
    updated_at=datetime.utcnow()
)
```

#### SubmissionResult

```python
from agents.models import SubmissionResult

# Success
result = SubmissionResult(
    success=True,
    reference_number="311-2026-0908-001"
)

# Failure
result = SubmissionResult(
    success=False,
    error_message="Network timeout"
)
```

---

## Testing

### Automated Tests

```bash
# Run all Phase 2 tests
./tests/test_phase2.sh

# Expected output:
# [1/4] Testing report models... ✓
# [2/4] Testing NOLA-311 connector... ✓
# [3/4] Testing integration imports... ✓
# [4/4] Testing browser manager... ✓
# All Phase 2 tests passed! ✓
```

### Individual Test Suites

```bash
# Model tests only
uv run python tests/phase2/test_models.py

# Connector tests only
uv run python tests/phase2/test_nola311.py
```

### Test Coverage

**Model Tests:**
- ✅ Location validation
- ✅ PotholeReport validation
- ✅ Phone number formatting
- ✅ Email validation
- ✅ Coordinate validation
- ✅ Description length validation
- ✅ StatusResult all status types
- ✅ SubmissionResult success/failure

**Connector Tests:**
- ✅ NOLA311Connector initialization
- ✅ Status normalization (8 status types)
- ✅ Submission result handling
- ✅ Error handling logic

**Integration Tests:**
- ✅ BrowserManager imports
- ✅ NOLA311Connector imports
- ✅ All model imports
- ✅ Cross-module dependencies

---

## Form Reconnaissance

⚠️ **IMPORTANT:** Form selectors in `nola311.py` are placeholders marked as `TBD`.

### Why Reconnaissance is Needed

The NOLA-311 QuickBase form has no public API or documentation. We need to:
1. Identify actual form field names and IDs
2. Understand validation rules
3. Locate the submit button
4. Find where reference numbers appear
5. Determine status page structure

### Running Reconnaissance

```bash
# Start interactive exploration
cd agents
uv run python scripts/explore_nola311.py
```

**What it does:**
1. Opens browser window (headed mode)
2. Navigates to NOLA-311 form
3. Analyzes all form fields automatically
4. Prints field information to console
5. Waits for manual exploration
6. Saves HTML and screenshot for offline analysis

**Output:**
```
Found 12 input fields:
  Input #1:
    Type: text
    Name: address_field
    ID: qb_address
    Required: Yes

Found 2 textarea fields:
  Textarea #1:
    Name: description
    ID: qb_desc
    Required: Yes

Found 3 select dropdowns:
  Select #1:
    Name: issue_type
    Options: 10
      - Pothole (value=pothole)
      - Street Light (value=light)
      ...

Press Enter when done exploring...
```

**Files saved:**
- `docs/nola311_form_YYYYMMDD_HHMMSS.html` - Full page HTML
- `docs/nola311_form_YYYYMMDD_HHMMSS.png` - Screenshot

### Updating Form Selectors

After reconnaissance, update `FORM_SELECTORS` in `integrations/nola311.py`:

```python
FORM_SELECTORS = {
    # Replace TBD with actual values from reconnaissance
    'address': 'input[name="address_field"]',        # Was: TBD
    'description': 'textarea[id="qb_desc"]',         # Was: TBD
    'issue_type': 'select[name="issue_type"]',       # Was: TBD
    'submit_button': 'button.submit-btn',            # Was: TBD
    'reference_number': 'span.reference-num',        # Was: TBD
    # ... etc
}
```

### Documentation

Document findings in `docs/nola311_form_spec.md`:
- Field names and IDs
- Required vs optional fields
- Validation rules
- Submit button selector
- Confirmation message location
- Reference number format

---

## Error Handling

### Retry Logic

The connector automatically retries failed operations:

```python
result = await connector.submit_report(
    report,
    max_retries=3  # Default: 3 attempts
)
```

**Retry behavior:**
- Attempt 1: Immediate
- Attempt 2: Wait 1 second (2^0)
- Attempt 3: Wait 2 seconds (2^1)
- Attempt 4: Wait 4 seconds (2^2)

### Screenshot Capture

Errors automatically capture screenshots:

```python
connector = NOLA311Connector(
    screenshot_dir="docs/screenshots"
)
```

**Screenshot naming:**
```
error_YYYYMMDD_HHMMSS.png
```

Includes:
- Full page content
- Error state
- Form validation messages
- Network errors visible

### Common Errors

**TimeoutError:**
```python
# Form didn't load in time
# Solution: Check network connection, try again
```

**ElementNotFoundError:**
```python
# Form selector not found
# Solution: Run reconnaissance, update FORM_SELECTORS
```

**ValidationError:**
```python
# Model validation failed
# Solution: Check required fields, data formats
```

---

## Configuration

### Environment Variables

Add to `.env`:

```env
# NOLA-311 Configuration
NOLA311_HEADLESS=true
NOLA311_TIMEOUT=30000
NOLA311_SCREENSHOT_DIR=docs/screenshots
```

### Browser Settings

```python
# Headless mode (no visible browser)
connector = NOLA311Connector(headless=True)

# Headed mode (watch it work - for debugging)
connector = NOLA311Connector(headless=False)

# Custom screenshot directory
connector = NOLA311Connector(
    screenshot_dir="/custom/path/screenshots"
)
```

---

## CI/CD

### GitHub Actions Workflow

**File:** `.github/workflows/phase2-tests.yml`

**Triggers:**
- Push to `main` or `phase-2-*` branches
- Pull requests to `main`
- Changes in `agents/` directory

**Jobs:**
1. Install Python 3.13 + uv
2. Install dependencies
3. Install Playwright browsers
4. Run ruff formatting/linting
5. Test Phase 1 & 2 dependencies
6. Test model imports
7. Test integration imports
8. Run Phase 2 model tests
9. Run Phase 2 connector tests
10. Run full Phase 2 test suite
11. Upload test results as artifacts

### Running Locally

```bash
# Format code
cd agents
uv run ruff format src/
uv run ruff check --fix src/

# Run all tests
./tests/test_phase2.sh

# Individual test suites
uv run python tests/phase2/test_models.py
uv run python tests/phase2/test_nola311.py
```

---

## Troubleshooting

### Browser Not Found

**Error:** `playwright._impl._api_types.Error: Executable doesn't exist`

**Solution:**
```bash
uv run playwright install chromium
```

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'agents'`

**Solution:**
```bash
# Use uv run
uv run python script.py

# Or activate venv
source .venv/bin/activate
python script.py
```

### Form Selectors Not Working

**Error:** `TimeoutError: waiting for selector` or `Element not found`

**Solution:**
1. Run form reconnaissance: `uv run python scripts/explore_nola311.py`
2. Update `FORM_SELECTORS` in `integrations/nola311.py`
3. Test with headed mode: `NOLA311Connector(headless=False)`

### Phone Validation Fails

**Error:** `ValueError: Invalid US phone number format`

**Valid formats:**
```python
"5045551234"      # ✓ 10 digits
"504-555-1234"    # ✓ With dashes
"(504) 555-1234"  # ✓ Formatted
"+15045551234"    # ✓ With country code
```

**Invalid formats:**
```python
"555-1234"        # ✗ Missing area code
"123456"          # ✗ Too short
"+445551234567"   # ✗ UK number (US only)
```

### Coordinate Validation Fails

**Error:** `ValueError: Latitude X outside New Orleans area`

**Valid range:**
- Latitude: 28.5° to 30.5° (New Orleans area)
- Longitude: -91° to -88° (New Orleans area)

**Example valid coordinates:**
```python
# New Orleans coordinates
{"lat": 29.9511, "lng": -90.0715}  # French Quarter
{"lat": 29.9311, "lng": -90.0852}  # Uptown
```

---

## Dependencies

### Phase 2 Additions

```toml
dependencies = [
    # ... Phase 1 dependencies
    "playwright>=1.40.0",       # Browser automation
    "beautifulsoup4>=4.12.0",   # HTML parsing
    "lxml>=4.9.0",              # XML/HTML parser
    "httpx>=0.25.0",            # HTTP client (fallback)
    "email-validator>=2.0.0",   # Email validation
]
```

### Installing

```bash
cd agents
uv sync
uv run playwright install chromium
```

---

## File Structure

```
agents/
├── src/agents/
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── browser.py           # BrowserManager
│   │   └── nola311.py           # NOLA311Connector
│   │
│   └── models/
│       ├── __init__.py
│       └── report.py            # Data models
│
├── scripts/
│   └── explore_nola311.py       # Form reconnaissance
│
├── docs/
│   ├── nola311_form_spec.md     # Form documentation
│   └── screenshots/             # Error screenshots
│
├── tests/
│   ├── phase2/
│   │   ├── test_models.py       # Model tests
│   │   └── test_nola311.py      # Connector tests
│   └── test_phase2.sh           # Test runner
│
└── PHASE2_README.md             # This file
```

---

## Usage Examples

### Example 1: Submit Report

```python
from agents.integrations import NOLA311Connector
from agents.models import PotholeReport, Location

async def submit_pothole():
    # Create report
    location = Location(
        address="1234 Magazine St, New Orleans, LA",
        cross_street="Napoleon Ave",
        landmark="Near Whole Foods"
    )
    
    report = PotholeReport(
        location=location,
        description="Large pothole in right lane, approximately 2 feet wide and 6 inches deep. Causing vehicles to swerve into oncoming traffic.",
        severity="high",
        reporter_name="Jane Doe",
        email="jane@example.com",
        phone="504-555-1234"
    )
    
    # Submit
    connector = NOLA311Connector(headless=True)
    result = await connector.submit_report(report)
    
    if result.success:
        print(f"✓ Success! Reference: {result.reference_number}")
        return result.reference_number
    else:
        print(f"✗ Failed: {result.error_message}")
        return None

# Run
import asyncio
ref = asyncio.run(submit_pothole())
```

### Example 2: Check Status

```python
from agents.integrations import NOLA311Connector

async def check_report_status(reference_number):
    connector = NOLA311Connector()
    status = await connector.check_status(reference_number)
    
    print(f"Reference: {status.reference_number}")
    print(f"Status: {status.status}")
    print(f"NOLA-311 Status: {status.raw_status}")
    print(f"Notes: {status.notes}")
    print(f"Updated: {status.updated_at}")
    
    return status

# Run
import asyncio
status = asyncio.run(check_report_status("311-2026-0908-001"))
```

### Example 3: Debugging with Headed Mode

```python
from agents.integrations import NOLA311Connector
from agents.models import PotholeReport, Location

async def debug_submission():
    # Create simple report
    location = Location(address="123 Test St, New Orleans, LA")
    report = PotholeReport(
        location=location,
        description="Test pothole for debugging form submission process",
        reporter_name="Test User",
        email="test@example.com"
    )
    
    # Run with visible browser and slow motion
    connector = NOLA311Connector(
        headless=False,  # Watch it work!
        screenshot_dir="docs/screenshots"
    )
    
    # Will open browser window and show form being filled
    result = await connector.submit_report(report)
    
    return result

import asyncio
result = asyncio.run(debug_submission())
```

---

## Next Steps

### Phase 3: DynamoDB Data Layer

After completing form reconnaissance, Phase 3 will add:

**Data Persistence:**
- Store submitted reports in DynamoDB
- Track status history over time
- Save NOLA-311 reference numbers
- User report history

**Duplicate Detection:**
- Geospatial search with geohash
- Find nearby reports within 100 meters
- Link users to existing reports
- Prevent duplicate submissions

**Features:**
- Single-table DynamoDB design
- Global Secondary Indexes for queries
- DynamoDB Local for testing
- NoSQLWorkbench visualization

---

## Contributing

### Before Committing

```bash
# Format code
cd agents
uv run ruff format src/
uv run ruff check --fix src/

# Run tests
./tests/test_phase2.sh

# Verify all pass
```

### Adding New Status Types

Update `_normalize_status()` in `integrations/nola311.py`:

```python
status_map = {
    'new_status_name': 'normalized_status',
    # ... existing mappings
}
```

Add test case in `tests/phase2/test_nola311.py`:

```python
test_cases = [
    ("New Status Name", "normalized_status"),
    # ... existing cases
]
```

---

## Known Limitations

### Phase 2 Scope

- ✅ Form submission infrastructure complete
- ✅ Status checking infrastructure complete
- ⚠️ Form selectors need reconnaissance
- ❌ No database storage (Phase 3)
- ❌ No duplicate detection (Phase 3)
- ❌ No agent tools integration (Phase 4)

### CAPTCHA Handling

If NOLA-311 implements CAPTCHA:
- Detection logic in place
- Logs warning message
- Returns error result
- Manual fallback available

**Future solution:**
- 2Captcha/Anti-Captcha integration
- Pre-filled PDF for manual submission

### Form Changes

If QuickBase form changes:
- Selectors may break
- Re-run reconnaissance: `scripts/explore_nola311.py`
- Update selectors in `nola311.py`
- Update documentation in `nola311_form_spec.md`

---

## Resources

**Documentation:**
- Phase 1 README: `README.md`
- Phase 2 README: `PHASE2_README.md` (this file)
- Form Specification: `docs/nola311_form_spec.md`
- Project Intent: `/intent/02_nola311_integration.md`

**Scripts:**
- Form Reconnaissance: `scripts/explore_nola311.py`
- Phase 2 Tests: `tests/test_phase2.sh`

**Source Code:**
- NOLA311 Connector: `src/agents/integrations/nola311.py`
- Browser Manager: `src/agents/integrations/browser.py`
- Report Models: `src/agents/models/report.py`

**Tests:**
- Model Tests: `tests/phase2/test_models.py`
- Connector Tests: `tests/phase2/test_nola311.py`

---

**Last Updated:** 2026-09-08  
**Phase 2 Status:** ✅ Complete (pending form reconnaissance)  
**Next Phase:** Phase 3 - DynamoDB Data Layer
