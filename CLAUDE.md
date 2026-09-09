# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**HoleeMoly** is an AI agent that helps New Orleans residents report potholes to NOLA-311 and closes the feedback loop by notifying them when reports are resolved. The system uses conversational AI to file reports, detect duplicates, and track status changes.

## Repository Structure

This is a **dual-repository project** with separate frontend and backend:

```
holeemoly/
├── agents/                  # Python FastAPI backend with Strands SDK
├── holeymoley_fe/          # Next.js 16.3.4 frontend (React 19, TypeScript)
├── intent/                 # Phase intent documents (00_*, 01_*, etc.)
├── .claude/
│   ├── plans/             # Implementation plans
│   └── skills/            # Custom skills (implement-phase)
└── .github/workflows/     # CI/CD for both backend and frontend
```

## Quick Start Commands

### Backend (Python/FastAPI)

All commands run from `/agents` directory:

```bash
# Install dependencies
uv sync

# Install Playwright browsers (required for NOLA-311 integration)
uv run playwright install chromium

# Run FastAPI server (port 8000)
make run-api
# or: uv run python -m agents.main
# or: make run-api-dev  # uvicorn with --reload

# Format code
make fmt
# or: uv run ruff format src/ && uv run ruff check --fix src/

# Run tests
./tests/test_phase1.sh      # Phase 1 tests
./tests/test_phase2.sh      # Phase 2 tests

# Test WebSocket chat (requires server running)
make test-chat

# View API docs
open http://localhost:8000/docs
```

### Frontend (Next.js)

All commands run from `/holeymoley_fe` directory:

```bash
# Install dependencies
bun install

# Run dev server (port 3000)
bun run dev

# Build for production
bun run build

# Run production build
bun run start

# Lint
bun run lint
```

### Running Single Tests

```bash
# Backend: Run individual test file
cd agents
uv run python tests/phase2/test_models.py
uv run python tests/phase2/test_nola311.py

# Frontend: Run specific test
cd holeymoley_fe
bun test <test-file-pattern>
```

## Architecture

### Three-Tier Stack

```
┌─────────────────────────────────────────┐
│    Next.js Frontend (Port 3000)         │
│    - Chat UI for pothole reporting      │
│    - Status dashboard                   │
│    - Notification display               │
└──────────────┬──────────────────────────┘
               │ HTTP/WebSocket
               ▼
┌─────────────────────────────────────────┐
│    FastAPI Backend (Port 8000)          │
│    - /api/chat (WebSocket)              │
│    - /api/reports                       │
│    - /api/status                        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Strands Agent (Conversation Handler) │
│    - AWS Bedrock (Claude Sonnet 4.6)    │
│    - Tool orchestration                 │
│    - Session management                 │
└──────┬──────────────────┬───────────────┘
       │                  │
       ▼                  ▼
┌──────────────┐    ┌─────────────────┐
│ NOLA-311     │    │ DynamoDB        │
│ Connector    │    │ (Phase 3)       │
│ (Playwright) │    │                 │
└──────────────┘    └─────────────────┘
```

### Backend Architecture (agents/)

**FastAPI Application** (`agents/src/agents/`):
- `main.py` - FastAPI app entry point, CORS setup, route registration
- `config.py` - Pydantic settings from environment variables
- `api/routes/` - WebSocket chat, health, and report endpoints
- `api/schemas/` - Pydantic request/response models
- `api/middleware/` - CORS configuration
- `agent/conversation.py` - Strands agent wrapper with session management

**NOLA-311 Integration** (`agents/src/agents/integrations/`):
- `nola311.py` - QuickBase form automation (submit reports, check status)
- `browser.py` - Persistent Playwright browser context manager

**Data Models** (`agents/src/agents/models/`):
- `report.py` - PotholeReport, Location, StatusResult, SubmissionResult
- Phone auto-formatting: "504-555-1234" → "(504) 555-1234"
- Email validation with `EmailStr`
- Coordinate validation for New Orleans area (lat: 28.5-30.5, lng: -91 to -88)

### Frontend Architecture (holeymoley_fe/)

**Next.js 16.3.4** with React 19 and TypeScript:
- `app/page.tsx` - Main chat interface (to be implemented)
- `app/dashboard/page.tsx` - User's report dashboard (to be implemented)
- `components/` - Reusable UI components
- `lib/api.ts` - API client for FastAPI backend

**Important**: This is Next.js 16.3.4 with breaking changes from previous versions. Always check `node_modules/next/dist/docs/` before writing Next.js code.

### Strands SDK Integration

**Conversation Agent** (`agents/src/agents/agent/conversation.py`):
- Each WebSocket connection creates a unique session
- Conversation history maintained per session
- Agent responses extracted via `.text` attribute from `AgentResult`
- AWS Bedrock model: `us.anthropic.claude-sonnet-4-6`

**Critical**: When getting agent responses, always extract the text:
```python
result = self.agent(message)
if hasattr(result, 'text'):
    response = result.text
elif hasattr(result, 'content'):
    response = result.content
else:
    response = str(result)
```

### NOLA-311 Integration (Playwright)

**No official API exists** - we use browser automation:
- Form submission via Playwright in headless Chrome
- Persistent browser context with cookie storage
- Exponential backoff retry (1s, 2s, 4s)
- Screenshot capture on errors → `agents/docs/screenshots/`
- Status normalization: "Open" → submitted, "In Progress" → in_progress, etc.

**Form reconnaissance workflow**:
1. Run `uv run python agents/scripts/explore_nola311.py`
2. Manually navigate and inspect form fields
3. Document findings in `agents/docs/nola311_form_spec.md`
4. Update `FORM_SELECTORS` in `agents/src/agents/integrations/nola311.py`

## Phase-Based Implementation

This project follows an **8-phase implementation plan** with structured workflow:

### Completed Phases

**Phase 1: FastAPI Backend Foundation** ✅
- FastAPI server with WebSocket support
- Strands SDK integration
- Health and config endpoints
- Session-based conversation management
- **Time:** ~6 hours | **Tasks:** 12/12 | **Tests:** 6/6 passing

**Phase 2: NOLA-311 Integration** ✅
- Playwright browser automation
- QuickBase form submission
- Status checking and normalization
- BrowserManager with persistent sessions
- **Time:** ~12 hours | **Tasks:** 10/10 | **Tests:** 7/7 passing

### Remaining Phases

- **Phase 3:** DynamoDB Data Layer (reports, users, geospatial duplicate detection)
- **Phase 4:** Strands Agent Tools (report_pothole, check_status, search_nearby)
- **Phase 5:** Next.js Chat Interface
- **Phase 6:** Notifications (SES email, SNS SMS, in-app)
- **Phase 7:** Background Status Polling (Lambda + EventBridge)
- **Phase 8:** MVP Polish & Deployment

### Implement Phase Skill

Use `/implement-phase` skill for all future phases. This skill documents the proven workflow:

1. **Intent Document** (30 min) - Create `intent/0X_phase_name.md`
2. **Task List** (15 min) - Create all tasks upfront with TaskCreate
3. **Implement** (6-10 hours) - Code, test imports, update task status
4. **Test Suite** (2-3 hours) - Create `tests/test_phaseX.sh` with 100% pass requirement
5. **CI/CD** (30 min) - Update `.github/workflows/phaseX-tests.yml`
6. **Documentation** (1-2 hours) - Create `agents/PHASEX_README.md`
7. **Commit** (15 min) - Detailed commit message with task summary

**Success criteria**: All tasks complete, 100% test pass rate, comprehensive README, CI/CD passing.

## Testing Strategy

### Backend Testing

**Phase 1 Tests** (`agents/tests/test_phase1.sh`):
- Dependencies import
- Configuration loading
- FastAPI app instantiation
- Health endpoint
- Config endpoint
- WebSocket connection

**Phase 2 Tests** (`agents/tests/test_phase2.sh`):
- Model validation (Location, PotholeReport, StatusResult)
- NOLA311Connector initialization
- Status normalization
- Browser manager
- Integration imports

**Run all tests**:
```bash
cd agents
./tests/test_phase1.sh && ./tests/test_phase2.sh
```

### Testing Philosophy

- **Test after each task** - Never accumulate untested code
- **Test imports immediately** - Catch module errors early
- **100% pass rate required** - No phase is complete with failing tests
- **Automated test scripts** - Color-coded output (green/red)
- **CI/CD verification** - GitHub Actions runs on every push

## Configuration Management

### Environment Variables

**Backend** (`agents/.env`):
```env
# AWS
BEDROCK_MODEL=us.anthropic.claude-sonnet-4-6
AWS_DEFAULT_PROFILE=default
AWS_REGION=us-east-1

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# DynamoDB (Phase 3)
DYNAMODB_TABLE=holeemoly-data
DYNAMODB_ENDPOINT=http://localhost:8000

# Logging
LOG_LEVEL=INFO
```

**Frontend** (`holeymoley_fe/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### AWS Setup Required

- AWS credentials configured (`~/.aws/credentials`)
- Bedrock access enabled in AWS account
- Claude Sonnet 4.6 model access granted
- Test: `aws sts get-caller-identity`

## Development Workflow

### Starting New Phase

1. **Read intent document**: `intent/0X_phase_name.md`
2. **Create tasks**: Use TaskCreate for all tasks upfront
3. **Follow implement-phase skill**: `/implement-phase` for structured workflow
4. **Test incrementally**: After each task completion
5. **Commit frequently**: Every 3-5 tasks or when tests pass
6. **Document thoroughly**: README is as important as code

### Working with the Backend

```bash
cd agents

# 1. Make changes
vim src/agents/api/routes/chat.py

# 2. Test import immediately
uv run python -c "from agents.api.routes import chat_router; print('✓')"

# 3. Format code
make fmt

# 4. Run relevant tests
./tests/test_phase1.sh

# 5. Start server to verify
make run-api

# 6. Test WebSocket in another terminal
make test-chat
```

### Working with the Frontend

```bash
cd holeymoley_fe

# 1. Make changes
vim app/page.tsx

# 2. Check TypeScript
bun run build  # or tsc --noEmit

# 3. Test locally
bun run dev

# 4. Open in browser
open http://localhost:3000
```

### Debugging

**Backend issues**:
```bash
# Check configuration
uv run python -c "from agents.config import get_settings; print(get_settings())"

# Test agent
uv run python -c "from agents.agent import get_agent; agent = get_agent(); print('✓')"

# Check imports
uv run python -c "from agents.integrations import NOLA311Connector; print('✓')"

# Enable debug logging
LOG_LEVEL=DEBUG make run-api
```

**NOLA-311 issues**:
- Check `agents/docs/screenshots/` for error screenshots
- Run form reconnaissance: `uv run python agents/scripts/explore_nola311.py`
- Review form spec: `agents/docs/nola311_form_spec.md`

## Critical Patterns

### Never use `git add -A` or `git add .`

**Why**: Can accidentally commit sensitive files (.env, credentials) or large binaries.

**Instead**: Stage files explicitly by name:
```bash
git add src/agents/api/routes/chat.py
git add tests/test_phase1.sh
```

### When venv issues occur

**Problem**: `ModuleNotFoundError` even after `uv sync`

**Solution**: Use `uv run` which handles venv automatically:
```bash
# Don't: source .venv/bin/activate && python ...
# Do:
uv run python -m agents.main
uv run python tests/phase2/test_models.py
```

### Commit Message Format

```
<type>: <short description>

<detailed explanation>

## Tasks Complete (X/X)
✅ Task #1: Description
✅ Task #2: Description

## Features/Changes
- Feature 1
- Feature 2

## Test Results
All tests passing ✅

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

### Code Formatting

**Always format before committing**:
```bash
cd agents
make fmt  # runs ruff format + ruff check --fix
```

CI will fail if code isn't formatted.

## Data Layer (Phase 3 - Not Yet Implemented)

### DynamoDB Single-Table Design

**Table**: `holeemoly-data`

**Access Patterns**:
- `USER#<user_id> / PROFILE` - User contact info and preferences
- `REPORT#<report_id> / METADATA` - Report details and status
- `REPORT#<report_id> / STATUS#<timestamp>` - Status change history
- `LOCATION#<geohash_6> / REPORT#<report_id>` - Spatial index for duplicates
- `USER#<user_id> / REPORT#<timestamp>` - User's reports index

**GSIs**:
- **StatusIndex** (PK: status, SK: last_checked) - Find active reports for polling
- **LocationIndex** (PK: geohash_6, SK: created_at) - Spatial queries

### Duplicate Detection (Phase 3)

Uses **geohash encoding** (6 chars = ~1.2km × 0.6km grid):
1. Geocode address to lat/lng (Google Maps API or Mapbox)
2. Generate 6-character geohash
3. Query DynamoDB LocationIndex
4. Calculate haversine distance
5. Flag as duplicate if within 100 meters and status not "resolved"

## Important Files

### Intent Documents

- `intent/00_project_overview.md` - Overall project vision
- `intent/01_fastapi_backend.md` - Phase 1 specification
- `intent/02_nola311_integration.md` - Phase 2 specification

### Backend Documentation

- `agents/README.md` - Phase 1 comprehensive guide
- `agents/PHASE2_README.md` - Phase 2 comprehensive guide (918 lines)
- `agents/docs/nola311_form_spec.md` - QuickBase form field reference

### Configuration

- `agents/.env.example` - Environment variable template
- `agents/pyproject.toml` - Python dependencies
- `agents/Makefile` - Common backend commands
- `holeymoley_fe/package.json` - Frontend dependencies

### Testing

- `agents/tests/test_phase1.sh` - Phase 1 automated test runner
- `agents/tests/test_phase2.sh` - Phase 2 automated test runner
- `agents/test_client.py` - WebSocket test client

## Cost Considerations

**Development (local)**: $0/month
- dynamodb-local for database
- AWS free tier for Bedrock testing

**Production (100 reports/month)**: ~$20/month
- DynamoDB: $1.50
- Lambda: $0.50
- SES: $0.03 (email)
- SNS: $1.00 (SMS opt-in)
- CloudWatch: $2.00
- Bedrock: $15.00 (Claude Sonnet 4.6)

**Production scale (1000 reports/month)**: ~$80/month

## Common Issues

### `ModuleNotFoundError: pydantic_settings`
```bash
cd agents
uv sync  # Reinstall dependencies
```

### `WebSocket connection refused`
```bash
# Make sure backend is running
cd agents
make run-api

# Check port availability
lsof -i :8000
```

### `Agent not responding`
```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify Bedrock access
aws bedrock list-foundation-models --region us-east-1

# Check model in .env
grep BEDROCK_MODEL agents/.env
```

### `Playwright browser not found`
```bash
cd agents
uv run playwright install chromium
uv run playwright install-deps chromium
```

### `Import errors`
```bash
# Run from correct directory
cd agents

# Use module syntax
uv run python -m agents.main

# Never use: python src/agents/main.py
```

## References

- **NOLA-311 Form**: https://opcd.quickbase.com/nav/app/bn79jh4a4/table/bn8jze2s7/action/nwr
- **Strands SDK**: https://docs.strands.ai/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Playwright**: https://playwright.dev/python/
- **Next.js 16.3 Docs**: `node_modules/next/dist/docs/` (breaking changes from previous versions)
- **Project Plan**: `.claude/plans/this-project-is-to-polished-turing.md`

## Success Metrics

- Number of reports filed through agent
- Duplicate detection accuracy
- Time from report to resolution notification
- User retention (repeat usage)
- NOLA-311 integration uptime (target: 95%+)
- Notification delivery rate (target: 98%+)
- Background polling success rate (target: 95%+)
