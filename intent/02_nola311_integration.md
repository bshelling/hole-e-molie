# Intent: NOLA-311 Integration with Playwright

## Phase

Phase 2 of 8

## Objective

Automate pothole report submission and status checking by integrating with NOLA-311's QuickBase system using Playwright browser automation.

## Problem Statement

NOLA-311 uses a QuickBase form for pothole reporting with no public API. We need to:
1. Submit pothole reports programmatically
2. Check status of existing reports
3. Extract reference numbers and status information

**NOLA-311 Form URL:** https://opcd.quickbase.com/nav/app/bn79jh4a4/table/bn8jze2s7/action/nwr?nexturl=%2Fdb%2Fbn79jh4a4%3Fa%3Dshowpage%26pageIdV2%3Dquickbase.com-DashboardGroup-9e8df6e8-4d3f-4dc9-918f-ce43c863dfda&page=3

## Scope

### In Scope

- Playwright browser automation setup
- QuickBase form reconnaissance and analysis
- Form field mapping and documentation
- Report submission automation
- Reference number extraction
- Status page scraping
- Status normalization (Open → submitted, etc.)
- Error handling and retry logic
- Screenshot capture for debugging
- Browser session management

### Out of Scope

- Database storage (Phase 3)
- Duplicate detection (Phase 3)
- Agent tools integration (Phase 4)
- Email/SMS notifications (Phase 6)
- Background polling (Phase 7)
- CAPTCHA solving (implement fallback if needed)

## Technical Requirements

### Dependencies to Add

```toml
dependencies = [
    # ... existing dependencies
    "playwright>=1.40.0",           # Browser automation
    "beautifulsoup4>=4.12.0",       # HTML parsing
    "lxml>=4.9.0",                  # XML/HTML parser
    "httpx>=0.25.0",                # HTTP client (fallback)
]
```

### Project Structure

```
agents/src/agents/
├── integrations/
│   ├── __init__.py
│   ├── nola311.py              # Main NOLA-311 connector
│   └── browser.py              # Browser context manager
│
├── models/
│   ├── __init__.py
│   └── report.py               # Enhanced report models
│
└── docs/
    └── nola311_form_spec.md    # Form field documentation
```

### Key Components

**1. NOLA311Connector Class**
```python
class NOLA311Connector:
    async def submit_report(report_data: PotholeReport) -> str:
        """Submit report and return NOLA-311 reference number"""
        
    async def check_status(reference_number: str) -> StatusResult:
        """Check status of existing report"""
        
    def _normalize_status(raw_status: str) -> str:
        """Map NOLA-311 status to internal states"""
```

**2. BrowserManager Class**
```python
class BrowserManager:
    """Manage persistent Playwright browser context"""
    async def __aenter__(self) -> BrowserContext
    async def __aexit__(...)
```

**3. Report Models**
```python
class PotholeReport(BaseModel):
    location: Location
    description: str
    severity: str
    reporter_name: str
    email: str
    phone: Optional[str]
    
class StatusResult(BaseModel):
    status: str
    notes: str
    updated_at: datetime
    reference_number: str
```

## Implementation Tasks

### Task 1: Setup and Dependencies (30 min)

1. Add Playwright and related packages to `pyproject.toml`
2. Run `uv sync`
3. Install Playwright browsers: `playwright install chromium`
4. Verify Playwright installation

### Task 2: Form Reconnaissance (2 hours)

**Goal:** Understand the QuickBase form structure

1. Create `scripts/explore_nola311.py` - interactive exploration script
2. Analyze form with Playwright in headed mode:
   - Navigate to form URL
   - Inspect all input fields (name, id, type)
   - Identify required vs optional fields
   - Check for hidden fields (CSRF tokens, session IDs)
   - Test manual submission flow
3. Document findings in `docs/nola311_form_spec.md`:
   - All field names and IDs
   - Required fields
   - Validation rules
   - Success/error indicators
   - Reference number location
4. Capture network requests (POST payload structure)

### Task 3: Browser Management (1 hour)

Create `integrations/browser.py`:

```python
class BrowserManager:
    """
    Persistent browser context with session management
    """
    - Initialize Playwright
    - Create browser context
    - Save/load session state
    - Handle browser lifecycle
```

**Features:**
- Persistent cookies in `nola311_session.json`
- Configurable viewport
- User agent string
- Headless mode toggle

### Task 4: Report Models (1 hour)

Create `models/report.py`:

```python
class Location(BaseModel):
    address: str
    coordinates: Optional[dict] = None
    landmark: Optional[str] = None

class PotholeReport(BaseModel):
    location: Location
    description: str
    severity: Literal["low", "medium", "high"]
    reporter_name: str
    email: EmailStr
    phone: Optional[str] = None
    
    @validator('phone')
    def validate_phone(cls, v):
        # Validate phone format
        
class StatusResult(BaseModel):
    status: str  # submitted, in_progress, resolved, duplicate
    notes: str
    updated_at: datetime
    reference_number: str
```

### Task 5: Form Submission (3 hours)

Create `integrations/nola311.py` with `submit_report()`:

**Steps:**
1. Initialize browser context
2. Navigate to form URL
3. Wait for form to load (`networkidle`)
4. Fill all required fields
5. Handle dropdowns/selects
6. Submit form
7. Wait for confirmation page
8. Extract reference number
9. Return reference number

**Error Handling:**
- Retry logic with exponential backoff
- Screenshot on error
- Timeout handling
- CAPTCHA detection (log warning, return None)

### Task 6: Status Checking (2 hours)

Implement `check_status()`:

**Steps:**
1. Navigate to status lookup page
2. Search by reference number
3. Parse status page HTML
4. Extract current status
5. Extract status notes
6. Extract last updated timestamp
7. Normalize status values
8. Return StatusResult

**Status Mapping:**
```python
STATUS_MAP = {
    'Open': 'submitted',
    'In Progress': 'in_progress',
    'Assigned': 'in_progress',
    'Closed': 'resolved',
    'Duplicate': 'duplicate',
    'Cancelled': 'closed'
}
```

### Task 7: Integration Testing (2 hours)

Create test suite:

**Tests:**
1. `test_nola311_form.py`:
   - Test form field detection
   - Test form filling
   - Test submission flow (mock)
   
2. `test_nola311_status.py`:
   - Test status lookup
   - Test status parsing
   - Test status normalization
   
3. `test_integration.py`:
   - End-to-end test with real submission (optional)
   - Test with test reference numbers

**Manual Testing:**
1. Submit test report via script
2. Verify report appears on NOLA-311 site
3. Check status via script
4. Verify status matches website

### Task 8: Error Handling & Resilience (1 hour)

Add:
- Rate limiting (respect NOLA-311 servers)
- Exponential backoff on errors
- Network timeout handling
- Form structure change detection
- Graceful degradation (fallback to manual submission)

### Task 9: Documentation (30 min)

Create:
- `docs/nola311_form_spec.md` - Form field reference
- Update `README.md` - Usage examples
- Add docstrings to all functions
- Create troubleshooting guide

### Task 10: CI/CD Updates (30 min)

Update `.github/workflows/` to include Phase 2 tests:
- Install Playwright browsers in CI
- Run form submission tests (mocked)
- Run status check tests

**Total Time Estimate:** 12-14 hours (2 days)

## Data Flow

```
┌─────────────────┐
│  FastAPI Agent  │
│  (Phase 1)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  NOLA311Connector       │
│  - submit_report()      │
│  - check_status()       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  BrowserManager         │
│  - Playwright context   │
│  - Session management   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  QuickBase Form         │
│  (NOLA-311 website)     │
└─────────────────────────┘
```

## Success Criteria

Phase 2 is complete when:

- [ ] Playwright and dependencies installed
- [ ] QuickBase form fully documented
- [ ] Browser manager handles sessions
- [ ] `submit_report()` successfully submits to NOLA-311
- [ ] Reference number extracted correctly
- [ ] `check_status()` retrieves and parses status
- [ ] Status values normalized correctly
- [ ] Error handling with retry logic
- [ ] Screenshots captured on errors
- [ ] All tests passing (unit + integration)
- [ ] Code formatted with ruff
- [ ] Documentation complete
- [ ] CI/CD workflow updated
- [ ] Changes committed to git
- [ ] PR created for review

## Testing Strategy

### Unit Tests

```python
# Test status normalization
def test_normalize_status():
    assert normalize_status("Open") == "submitted"
    assert normalize_status("In Progress") == "in_progress"
    
# Test form field mapping
def test_form_fields():
    fields = await connector.get_form_fields()
    assert "address" in fields
    assert "description" in fields
```

### Integration Tests

```python
# Test full submission flow (mocked)
async def test_submit_report_mock():
    report = PotholeReport(...)
    ref = await connector.submit_report(report)
    assert ref.startswith("311-")
    
# Test status check
async def test_check_status():
    result = await connector.check_status("311-2026-0908-001")
    assert result.status in ["submitted", "in_progress", "resolved"]
```

### Manual Verification

1. Submit test report via script
2. Verify on NOLA-311 website
3. Check status via script
4. Compare with website status

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Form structure changes | High | High | Document all fields, implement field discovery, add alerting |
| CAPTCHA implemented | Medium | High | Detect CAPTCHA, implement 2Captcha fallback, provide manual submission option |
| Rate limiting | Medium | Medium | Implement backoff, respect rate limits, add delay between requests |
| Network failures | High | Low | Retry logic, timeout handling, graceful error messages |
| Session expiration | Medium | Low | Persistent session management, automatic session refresh |

## Known Limitations

- No CAPTCHA solving (will implement fallback if needed)
- No database storage yet (Phase 3)
- No duplicate detection yet (Phase 3)
- Manual testing required for initial form analysis
- May need adjustments if QuickBase form changes

## Integration Points

### With Phase 1 (FastAPI)

- NOLA311Connector will be used by agent tools (Phase 4)
- Status results will be returned via API endpoints
- Error handling will propagate to WebSocket responses

### For Phase 3 (Database)

- Report models will be stored in DynamoDB
- Reference numbers will be saved
- Status updates will be tracked

### For Phase 4 (Agent Tools)

- `submit_report()` will be called by `report_pothole` tool
- `check_status()` will be called by `check_status` tool
- Results will be formatted for conversational responses

## Environment Variables

Add to `.env`:

```env
# NOLA-311 Configuration
NOLA311_FORM_URL=https://opcd.quickbase.com/nav/app/...
NOLA311_STATUS_URL=https://opcd.quickbase.com/status
NOLA311_HEADLESS=true
NOLA311_TIMEOUT=30000
```

## Dependencies

```toml
[project]
dependencies = [
    # Phase 1 dependencies...
    "playwright>=1.40.0",
    "beautifulsoup4>=4.12.0",
    "lxml>=4.9.0",
    "httpx>=0.25.0",
]
```

## Next Phase

**Phase 3:** DynamoDB Data Layer
- Store submitted reports
- Track status history
- Implement duplicate detection

## References

- **NOLA-311 Form:** https://opcd.quickbase.com/nav/app/bn79jh4a4/...
- **Playwright Docs:** https://playwright.dev/python/
- **QuickBase API:** (No public API available)
