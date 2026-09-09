---
name: implement-phase
description: Structured workflow for implementing project phases with intent, tasks, testing, and documentation
---

# Implement Phase Workflow

This skill guides the implementation of project phases using a proven workflow from Phases 1 and 2.

## When to Use

Use this skill when:
- Starting a new phase of the project (Phase 3, 4, 5, etc.)
- Implementing a major feature requiring multiple tasks
- Need structured approach with testing and documentation
- Want consistent implementation pattern across phases

## Workflow Overview

```
1. Intent → 2. Tasks → 3. Implement → 4. Test → 5. Document → 6. Commit
```

## Step-by-Step Process

### Step 1: Create Intent Document (30 min)

**File:** `intent/0X_phase_name.md` where X is the phase number

**Include:**
- **Phase:** Number of total phases (e.g., "Phase 3 of 8")
- **Objective:** What this phase accomplishes
- **Scope:** What's in scope and out of scope
- **Technical Requirements:** Dependencies, architecture, data models
- **Implementation Tasks:** 8-12 tasks with time estimates
- **Success Criteria:** Checklist of completion requirements
- **Testing Strategy:** How to verify success
- **Integration Points:** How this connects to other phases

**Template:**
```markdown
# Intent: [Phase Name]

## Phase
Phase X of Y

## Objective
[What this phase accomplishes in 1-2 sentences]

## Scope
### In Scope
- Feature 1
- Feature 2

### Out of Scope
- Feature A (Phase Y)
- Feature B (Phase Z)

## Technical Requirements
- Dependency 1
- Dependency 2

## Implementation Tasks
1. Task 1 (time estimate)
2. Task 2 (time estimate)
...

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
...

## Testing Strategy
- Test approach 1
- Test approach 2

## Next Phase
Phase X+1: [Name and brief description]
```

**Commit:** Commit intent document before starting implementation

### Step 2: Create Task List (15 min)

Use `TaskCreate` for each implementation task:

```
TaskCreate(
  subject="Task title in imperative form",
  description="Detailed description with file paths and specifics",
  activeForm="Present continuous (e.g., 'Creating models')"
)
```

**Guidelines:**
- 8-12 tasks per phase
- Each task should be completable in 30-90 minutes
- Use clear, actionable subjects
- Include file paths in descriptions
- Create all tasks upfront before starting

**Example Task Sequence:**
1. Add dependencies
2. Create directory structure
3. Implement configuration
4. Create data models
5. Build core functionality
6. Add error handling
7. Create test suite
8. Update CI/CD workflow

### Step 3: Implement Tasks Incrementally (varies)

For each task:

1. **Mark task as in progress:**
   ```
   TaskUpdate(taskId="X", status="in_progress")
   ```

2. **Implement the task:**
   - Write code
   - Follow existing patterns
   - Keep it focused on single task

3. **Test immediately:**
   - Import test: `uv run python -c "from module import Class"`
   - Unit test if applicable
   - Manual verification

4. **Mark task as complete:**
   ```
   TaskUpdate(taskId="X", status="completed")
   ```

5. **Commit progress every 3-5 tasks:**
   - Group related changes
   - Write descriptive commit message
   - Include what's working

**Best Practices:**
- Test imports immediately after creating modules
- Fix errors before moving to next task
- Commit working code frequently
- Update task status in real-time

### Step 4: Create Test Suite (2-3 hours)

**Structure:**
```
tests/
├── phaseX/
│   ├── test_models.py      # Model/data tests
│   ├── test_integration.py # Integration tests
│   └── test_feature.py     # Feature-specific tests
└── test_phaseX.sh          # Automated test runner
```

**Test Script Requirements:**
- Runs all test files
- Color-coded output (green/red/yellow)
- Exit code 0 on success, 1 on failure
- Clear error messages
- Summary at the end

**Example test_phaseX.sh:**
```bash
#!/bin/bash
set -e

echo "Phase X Tests"
echo "============="

# Test 1
echo "[1/4] Testing models..."
uv run python tests/phaseX/test_models.py && \
echo "✓ Passed" || exit 1

# Test 2
echo "[2/4] Testing integration..."
uv run python tests/phaseX/test_integration.py && \
echo "✓ Passed" || exit 1

# ... etc

echo "All tests passed!"
```

**Run tests:**
```bash
chmod +x tests/test_phaseX.sh
./tests/test_phaseX.sh
```

**All tests must pass before proceeding to documentation.**

### Step 5: Update CI/CD Workflow (30 min)

**File:** `.github/workflows/phaseX-tests.yml`

**Include:**
- Install dependencies
- Install any special tools (Playwright, etc.)
- Run ruff formatting/linting
- Test all imports
- Run phase-specific tests
- Upload test results as artifacts

**Copy from previous phase and adapt.**

### Step 6: Create Comprehensive README (1-2 hours)

**File:** `agents/PHASEX_README.md`

**Sections:**
1. **Overview**
   - Status (Complete/In Progress)
   - What was built
   - Key features

2. **Quick Start**
   - Prerequisites
   - Installation
   - Basic usage with code examples

3. **Architecture**
   - Component diagram
   - Data flow
   - Integration points

4. **API Reference**
   - Classes and methods
   - Parameters and return types
   - Usage examples

5. **Configuration**
   - Environment variables
   - Settings and options

6. **Testing**
   - How to run tests
   - Test coverage
   - Manual verification steps

7. **Troubleshooting**
   - Common errors and solutions
   - Debug tips

8. **Usage Examples**
   - 2-3 complete code examples
   - Cover main use cases

9. **Known Limitations**
   - What's not implemented (by design)
   - What needs manual steps

10. **Next Steps**
    - Preview of next phase

**Best Practices:**
- Include actual code examples that work
- Use clear, concise language
- Add code comments in examples
- Include command-line examples
- Cross-reference related docs

### Step 7: Final Commit and Push (15 min)

**Commit Message Format:**
```
Complete Phase X: [Phase Name] ✅

[1-2 paragraph summary of what was implemented]

## All Tasks Complete (X/X) ✅

✅ Task #1: Description
✅ Task #2: Description
...

## Features Implemented

- Feature 1
- Feature 2
...

## Test Results

All tests passing ✅

[Test summary]

## Files Created

- file1.py (X lines)
- file2.py (Y lines)
...

## Dependencies Added

- dependency1>=version
- dependency2>=version

## Next Steps

Phase X+1: [Brief description]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Push to main:**
```bash
git push origin main
```

## Success Criteria

Phase is complete when:

- ✅ Intent document created and committed
- ✅ All tasks created and tracked
- ✅ All tasks completed (100%)
- ✅ All tests passing (100%)
- ✅ CI/CD workflow updated and passing
- ✅ Comprehensive README created
- ✅ Code formatted with ruff
- ✅ Changes committed with detailed message
- ✅ Pushed to main branch

## Time Estimates by Phase Component

| Component | Time |
|-----------|------|
| Intent Document | 30 min |
| Task Creation | 15 min |
| Implementation | 6-10 hours |
| Test Suite | 2-3 hours |
| CI/CD Updates | 30 min |
| README | 1-2 hours |
| Final Commit | 15 min |
| **Total** | **10-16 hours** |

## Examples from This Project

### Phase 1: FastAPI Backend Foundation

**Results:**
- 12 tasks completed
- FastAPI server with WebSocket
- Strands SDK integration
- 100% test pass rate
- Comprehensive README

**Time:** ~6 hours

### Phase 2: NOLA-311 Integration

**Results:**
- 10 tasks completed
- Browser automation with Playwright
- Form submission & status checking
- 100% test pass rate
- Comprehensive README

**Time:** ~12 hours

## Best Practices

### Do's

✅ **Create intent before coding** - Plan first, implement second
✅ **Track all tasks** - Use task system to show progress
✅ **Test immediately** - Catch errors early
✅ **Commit frequently** - Every 3-5 tasks or 1-2 hours
✅ **Document thoroughly** - README is as important as code
✅ **Update CI/CD** - Automate testing
✅ **Follow patterns** - Maintain consistency across phases

### Don'ts

❌ **Don't skip intent** - Planning prevents rework
❌ **Don't skip testing** - Untested code = broken code
❌ **Don't skip documentation** - Future you will thank you
❌ **Don't commit untested code** - Test before commit
❌ **Don't batch all commits** - Incremental is better
❌ **Don't skip CI/CD** - Automated tests catch issues

## Common Pitfalls

### 1. Skipping Planning

**Problem:** Start coding without clear intent

**Solution:** Always create intent document first

### 2. Not Tracking Tasks

**Problem:** Lose track of progress, forget steps

**Solution:** Create all tasks upfront, update status

### 3. Not Testing Along the Way

**Problem:** Accumulate errors, hard to debug

**Solution:** Test after each task completion

### 4. Forgetting Documentation

**Problem:** No one knows how to use it later

**Solution:** Write README as you implement

### 5. Inconsistent Commit Messages

**Problem:** Hard to understand history

**Solution:** Follow commit message template

## Adapting for Different Phase Types

### For Backend Phases (API, Database, etc.)

- Focus on data models and schemas
- Include API endpoint documentation
- Add database schema diagrams
- Test CRUD operations thoroughly

### For Frontend Phases (UI, Components, etc.)

- Include component hierarchy
- Add screenshots or mockups
- Document props and state
- Test user interactions

### For Integration Phases (External APIs, etc.)

- Document external dependencies
- Include authentication flow
- Add error handling for external failures
- Mock external services in tests

## Template Files

### Intent Template

See Step 1 above for complete template.

### Test Script Template

```bash
#!/bin/bash
set -e
echo "Phase X Tests"
echo "============="

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

cd "$(dirname "$0")/.."
echo "Working directory: $(pwd)"

# Test imports
echo "[1/N] Testing imports..."
uv run python -c "from module import Class" && \
echo -e "${GREEN}✓ Passed${NC}" || \
{ echo -e "${RED}✗ Failed${NC}"; exit 1; }

# ... more tests

echo "All tests passed!"
```

### CI/CD Template

```yaml
name: Phase X - Tests

on:
  push:
    branches: [ main, phase-X-* ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./agents
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.13'
    - uses: astral-sh/setup-uv@v5
    
    - run: uv sync
    - run: uv run ruff format --check src/
    - run: ./tests/test_phaseX.sh
```

## Verification Checklist

Use this checklist to verify phase completion:

```
Phase X Implementation Checklist

Planning:
□ Intent document created (intent/0X_phase_name.md)
□ Intent committed to git
□ All tasks created (8-12 tasks)
□ Time estimates included

Implementation:
□ All tasks marked in_progress → completed
□ Code follows existing patterns
□ Imports tested after each module
□ Dependencies added to pyproject.toml
□ All dependencies installed (uv sync)

Testing:
□ Test files created (tests/phaseX/)
□ Test runner created (tests/test_phaseX.sh)
□ All tests passing locally
□ Test coverage adequate (>80%)

CI/CD:
□ GitHub Actions workflow created
□ Workflow tested and passing
□ Test artifacts uploaded

Documentation:
□ README created (PHASEX_README.md)
□ API reference complete
□ Usage examples included
□ Troubleshooting section added
□ Known limitations documented

Quality:
□ Code formatted with ruff
□ No linting errors
□ Error handling implemented
□ Logging added where appropriate

Version Control:
□ Changes committed with detailed message
□ Commit message follows template
□ Pushed to main branch
□ No merge conflicts

Handoff:
□ Status verified with user
□ All tests demonstrated
□ Next phase preview provided
```

## Getting Started

To implement a new phase:

```bash
# 1. Invoke this skill
/implement-phase

# 2. Or ask directly
"Let's implement Phase X following the standard workflow"

# 3. Provide phase details
- Phase number and name
- High-level objectives
- Key features to implement
```

The skill will guide you through each step systematically.

## Success Metrics

Track these metrics for each phase:

- **Planning time:** ~30-45 minutes
- **Implementation time:** 6-10 hours
- **Testing time:** 2-3 hours
- **Documentation time:** 1-2 hours
- **Tasks completed:** 100%
- **Test pass rate:** 100%
- **Code coverage:** >80%
- **Commits:** 3-5 per phase
- **Documentation:** Complete README

## Conclusion

This workflow has been proven successful for:
- Phase 1: FastAPI Backend (12 tasks, 100% success)
- Phase 2: NOLA-311 Integration (10 tasks, 100% success)

Following this pattern ensures:
- Structured implementation
- Comprehensive testing
- Complete documentation
- Smooth handoffs between phases
- Maintainable codebase

Use this skill for all future phases to maintain consistency and quality.
