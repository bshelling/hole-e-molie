# NOLA-311 QuickBase Form Specification

**Last Updated:** 2026-09-08  
**Form URL:** https://opcd.quickbase.com/nav/app/bn79jh4a4/table/bn8jze2s7/action/nwr?nexturl=%2Fdb%2Fbn79jh4a4%3Fa%3Dshowpage%26pageIdV2%3Dquickbase.com-DashboardGroup-9e8df6e8-4d3f-4dc9-918f-ce43c863dfda&page=3

## Overview

This document contains the complete specification of the NOLA-311 pothole reporting form for automation purposes.

**Status:** 🚧 In Progress - Needs Manual Exploration

Run `scripts/explore_nola311.py` to analyze the form and complete this specification.

---

## Form Fields

### Text Inputs

| Field Name | ID | Type | Required | Placeholder | Notes |
|------------|-----|------|----------|-------------|-------|
| TBD | TBD | text | ? | ? | To be determined after reconnaissance |

### Textareas

| Field Name | ID | Required | Placeholder | Max Length | Notes |
|------------|-----|----------|-------------|------------|-------|
| TBD | TBD | ? | ? | ? | To be determined |

### Select Dropdowns

| Field Name | ID | Required | Options | Default | Notes |
|------------|-----|----------|---------|---------|-------|
| TBD | TBD | ? | ? | ? | To be determined |

### Checkboxes / Radio Buttons

| Field Name | ID | Type | Required | Options | Notes |
|------------|-----|------|----------|---------|-------|
| TBD | TBD | ? | ? | ? | To be determined |

### Hidden Fields

| Field Name | ID | Value | Purpose | Notes |
|------------|-----|-------|---------|-------|
| TBD | TBD | ? | ? | Check for CSRF tokens, session IDs |

---

## Form Structure

### Expected Fields (Based on Requirements)

Based on pothole reporting requirements, we expect:

1. **Location Information:**
   - Street address
   - Cross street (optional)
   - Landmarks (optional)
   - Geographic coordinates (if collected)

2. **Issue Description:**
   - Description/details textarea
   - Issue type dropdown (should include "Pothole")
   - Severity/priority level

3. **Reporter Information:**
   - Name
   - Email
   - Phone (optional)
   - Preferred contact method

4. **Additional Information:**
   - Photo upload (if available)
   - Date noticed
   - Any reference numbers

---

## Validation Rules

### Client-Side Validation

- **Required Fields:** TBD
- **Email Format:** Standard email validation
- **Phone Format:** TBD (US phone number format?)
- **Address Validation:** TBD

### Server-Side Validation

To be determined by observing POST request responses.

---

## Submission Flow

### Step 1: Form Load

1. Navigate to form URL
2. Wait for page load
3. Check for any popups/modals
4. Verify form is visible

### Step 2: Form Filling

1. Fill required fields in order
2. Handle any dynamic field behaviors
3. Deal with dropdowns/selects
4. Upload files if needed

### Step 3: Form Submission

1. Click submit button
2. Wait for response
3. Handle loading states
4. Detect success/error

### Step 4: Confirmation

1. Identify confirmation page/message
2. Extract reference number
3. Save confirmation details

---

## Success Indicators

### Successful Submission

- **URL Change:** Does the page redirect after submission?
- **Confirmation Message:** What text appears on success?
- **Reference Number:** Where is it displayed? Format?
- **HTTP Status:** Expected: 200 or 302 (redirect)

### Error Indicators

- **Validation Errors:** How are they displayed?
- **Server Errors:** Error message format?
- **Network Errors:** Timeout handling?

---

## Reference Number Format

**Pattern:** TBD (e.g., `311-YYYY-MMDD-NNN`)

**Location:** TBD (confirmation page, email, modal?)

**Extraction Strategy:** TBD

---

## Status Checking

### Status Lookup Method

- **URL:** TBD
- **Method:** TBD (Form submission? URL parameter? API?)
- **Input:** Reference number
- **Authentication:** TBD (Required? Session-based?)

### Status Values

Map NOLA-311 status values to internal states:

| NOLA-311 Status | Internal Status | Description |
|----------------|-----------------|-------------|
| Open | submitted | Report received, not yet assigned |
| In Progress | in_progress | Work has begun |
| Assigned | in_progress | Crew assigned |
| Closed | resolved | Issue fixed |
| Duplicate | duplicate | Marked as duplicate |
| Cancelled | closed | Request cancelled |
| TBD | TBD | Additional states to be discovered |

---

## Network Analysis

### POST Request

**Endpoint:** TBD

**Method:** POST

**Headers:**
```
Content-Type: TBD
Cookie: TBD
CSRF-Token: TBD (if applicable)
```

**Payload Structure:**
```json
{
  "field1": "value1",
  "field2": "value2",
  ...
}
```

**Response:**
```json
{
  "success": true,
  "reference": "311-...",
  "message": "..."
}
```

---

## JavaScript/Dynamic Behaviors

### Form Initialization

- **Scripts:** TBD
- **Ajax Calls:** TBD
- **Event Listeners:** TBD

### Field Dependencies

- **Conditional Fields:** TBD (fields that appear based on other selections)
- **Auto-fill:** TBD (fields that auto-populate)
- **Validation Triggers:** TBD (real-time vs on-submit)

---

## CAPTCHA / Bot Protection

**Present:** TBD

**Type:** TBD (reCAPTCHA, hCaptcha, custom?)

**Trigger:** TBD (Always? After N submissions? Random?)

**Mitigation Strategy:**
- If CAPTCHA present: Implement 2Captcha/Anti-Captcha integration
- Fallback: Provide pre-filled form for manual submission

---

## Session Management

**Cookies Required:** TBD

**Session Timeout:** TBD

**Authentication:** TBD (Public form or login required?)

---

## Browser Requirements

**Minimum Browser:** Modern browsers (Chrome, Firefox, Safari, Edge)

**JavaScript Required:** TBD (likely yes for QuickBase)

**Cookies Required:** TBD

**User Agent:** Standard browser user agent

---

## Testing Strategy

### Test Cases

1. **Valid Submission:**
   - Fill all required fields with valid data
   - Submit and verify reference number

2. **Invalid Data:**
   - Missing required fields
   - Invalid email format
   - Invalid phone format

3. **Boundary Cases:**
   - Very long descriptions
   - Special characters in address
   - Multiple rapid submissions

4. **Error Handling:**
   - Network timeout
   - Server error
   - Invalid response

---

## Automation Checklist

Before implementing automation:

- [ ] All form fields documented
- [ ] Required fields identified
- [ ] Validation rules understood
- [ ] Submit button selector identified
- [ ] Success indicators documented
- [ ] Reference number extraction pattern known
- [ ] Error handling scenarios identified
- [ ] CAPTCHA presence confirmed/denied
- [ ] Network request structure documented
- [ ] Status check method identified

---

## Implementation Notes

### Playwright Selectors

```python
# To be filled after exploration
ADDRESS_INPUT = 'input[name="..."]'
DESCRIPTION_TEXTAREA = 'textarea[name="..."]'
SUBMIT_BUTTON = 'button[type="submit"]'
```

### Retry Strategy

- **Max Retries:** 3
- **Backoff:** Exponential (1s, 2s, 4s)
- **Timeout:** 30 seconds per attempt

### Screenshot Strategy

- **On Error:** Always capture screenshot
- **On Success:** Optional
- **Full Page:** Yes
- **Location:** `docs/screenshots/`

---

## Exploration Script Output

Run the exploration script and paste output here:

```bash
uv run python scripts/explore_nola311.py
```

**Output:** TBD

---

## Manual Exploration Notes

### Date: TBD

**Findings:**
- TBD

**Observations:**
- TBD

**Challenges:**
- TBD

**Recommendations:**
- TBD

---

## Next Steps

1. ✅ Create exploration script
2. ⏳ Run exploration script manually
3. ⏳ Fill in all TBD sections above
4. ⏳ Update implementation based on findings
5. ⏳ Create browser manager
6. ⏳ Implement form submission
7. ⏳ Implement status checking
8. ⏳ Add comprehensive tests

---

**Status:** 🚧 Template Complete - Awaiting Manual Form Exploration
