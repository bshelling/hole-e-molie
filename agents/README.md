# HoleeMoly Backend - FastAPI + Strands SDK

**Phase 1: FastAPI Backend Foundation** ✅ Complete

Backend API for NOLA pothole reporting and tracking agent using FastAPI and Strands SDK.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- AWS credentials configured (for Bedrock access)

### Installation

```bash
# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Edit .env with your AWS configuration
# BEDROCK_MODEL=us.anthropic.claude-sonnet-4-6
# AWS_DEFAULT_PROFILE=default
```

### Running the Server

```bash
# Start development server
make run-api

# Or use uvicorn directly
uv run uvicorn agents.main:app --reload --port 8000
```

Server starts at: **http://localhost:8000**

---

## 📚 API Documentation

### Interactive Docs

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/docs` | GET | Swagger UI |
| `/api/health` | GET | Health check |
| `/api/config` | GET | Configuration info |
| `/api/chat` | WebSocket | Real-time chat with agent |
| `/api/reports` | GET | List reports (placeholder) |
| `/api/reports/{id}` | GET | Get report by ID (placeholder) |

### WebSocket Chat

Connect to `ws://localhost:8000/api/chat` for real-time conversation with the Strands agent.

**Client sends:**
```json
{
  "type": "message",
  "content": "There's a pothole on Magazine Street"
}
```

**Server sends:**
```json
{
  "type": "assistant",
  "content": "Agent response here...",
  "session_id": "unique-session-id"
}
```

---

## 🧪 Testing

### Automated Tests

```bash
# Run full test suite
./tests/test_phase1.sh

# Expected output:
# [1/6] Testing dependencies... ✓
# [2/6] Testing configuration... ✓
# [3/6] Testing FastAPI app... ✓
# [4/6] Starting API server...
# [5/6] Testing health endpoint... ✓
# [6/6] Testing config endpoint... ✓
# All Phase 1 tests passed! ✓
```

### WebSocket Test Client

```bash
# Terminal 1: Start server
make run-api

# Terminal 2: Test WebSocket
make test-chat

# Expected output:
# [SYSTEM] Connected to HoleeMoly agent...
# [YOU] Hello, I want to report a pothole
# [AGENT] Hello! I'd be happy to help...
# ✓ All test messages sent successfully!
```

### Manual Testing

```bash
# Health check
curl http://localhost:8000/api/health

# Configuration
curl http://localhost:8000/api/config

# Reports (placeholder)
curl http://localhost:8000/api/reports
```

---

## 📁 Project Structure

```
agents/
├── src/agents/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Pydantic settings & env vars
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── chat.py      # WebSocket chat endpoint
│   │   │   ├── health.py    # Health & config endpoints
│   │   │   └── reports.py   # Report endpoints (placeholder)
│   │   │
│   │   ├── schemas/
│   │   │   ├── message.py   # Chat message models
│   │   │   └── report.py    # Report models (placeholder)
│   │   │
│   │   └── middleware/
│   │       └── cors.py      # CORS configuration
│   │
│   └── agent/
│       └── conversation.py  # Strands agent wrapper
│
├── tests/
│   └── test_phase1.sh       # Automated test suite
│
├── test_client.py           # WebSocket test client
├── .env.example             # Environment variables template
├── pyproject.toml           # Dependencies & project config
├── Makefile                 # Common commands
└── README.md                # This file
```

---

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# AWS Configuration
BEDROCK_MODEL=us.anthropic.claude-sonnet-4-6
AWS_DEFAULT_PROFILE=default
AWS_REGION=us-east-1

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Logging
LOG_LEVEL=INFO
```

### AWS Setup

The agent uses **AWS Bedrock** with **Claude Sonnet 4.6**. Ensure you have:

1. AWS credentials configured (`~/.aws/credentials`)
2. Bedrock access enabled in your AWS account
3. Claude model access granted

---

## 🛠️ Development

### Makefile Commands

```bash
make run-api        # Start FastAPI server
make run-api-dev    # Start with uvicorn --reload
make test-chat      # Test WebSocket client
make fmt            # Format code with ruff
make fmtrun-api     # Format then run
make install        # Install dependencies
make clean          # Clean Python cache files
```

### Code Formatting

```bash
# Format code
uv run ruff format src/

# Check and auto-fix issues
uv run ruff check --fix src/
```

---

## 🏗️ Architecture

### Tech Stack

- **FastAPI** - Modern async web framework
- **Strands SDK** - Agent framework with tool support
- **AWS Bedrock** - Claude Sonnet 4.6 LLM
- **Pydantic** - Data validation and settings
- **WebSockets** - Real-time bidirectional communication

### Component Flow

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ WebSocket
       ▼
┌─────────────────────┐
│  FastAPI Server     │
│  - CORS middleware  │
│  - Route handlers   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ ConversationAgent   │
│ - Session manager   │
│ - Message history   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   Strands Agent     │
│   - AWS Bedrock     │
│   - Claude Model    │
└─────────────────────┘
```

### Session Management

- Each WebSocket connection gets a unique session ID
- Conversation history is maintained per session
- Sessions are cleaned up on disconnect

---

## ✅ Phase 1 Status

### Completed Features

- ✅ FastAPI application with WebSocket support
- ✅ Strands SDK integration with AWS Bedrock
- ✅ Real-time chat endpoint (`/api/chat`)
- ✅ Health and configuration endpoints
- ✅ CORS middleware for Next.js frontend
- ✅ Session-based conversation management
- ✅ Pydantic configuration with environment variables
- ✅ Automated test suite
- ✅ WebSocket test client
- ✅ CI/CD workflow (GitHub Actions)
- ✅ Code formatting with ruff

### Test Results

All tests passing ✅

| Test | Status |
|------|--------|
| Dependencies | ✅ PASS |
| Configuration | ✅ PASS |
| FastAPI App | ✅ PASS |
| Health Endpoint | ✅ PASS |
| Config Endpoint | ✅ PASS |
| WebSocket Connection | ✅ PASS |
| Agent Response | ✅ PASS |
| Session Management | ✅ PASS |

See `PHASE1_TEST_RESULTS.md` for detailed test documentation.

---

## 🚧 Known Limitations (By Design)

These features are **intentionally not implemented** in Phase 1 and will be added in future phases:

| Feature | Status | Phase |
|---------|--------|-------|
| NOLA-311 Integration | ❌ Not Implemented | Phase 2 |
| Database Storage (DynamoDB) | ❌ Not Implemented | Phase 3 |
| Duplicate Detection | ❌ Not Implemented | Phase 3 |
| Agent Tools (report_pothole, etc.) | ❌ Not Implemented | Phase 4 |
| Next.js Frontend Connection | ❌ Not Implemented | Phase 5 |
| Email/SMS Notifications | ❌ Not Implemented | Phase 6 |
| Background Status Polling | ❌ Not Implemented | Phase 7 |

**Phase 1 Focus:** API infrastructure only ✅

---

## 🔧 Troubleshooting

### Server won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
uv sync  # Reinstall dependencies
```

### WebSocket connection fails

**Error:** `Connection refused`

**Solution:**
```bash
# Make sure server is running
make run-api

# Check if port 8000 is available
lsof -i :8000
```

### Agent not responding

**Error:** `Error getting agent response`

**Solution:**
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify Bedrock access in AWS Console
3. Check `BEDROCK_MODEL` in `.env`
4. Ensure Claude model access is enabled

### Import errors

**Error:** `ImportError: attempted relative import with no known parent package`

**Solution:**
```bash
# Run from agents directory
cd /path/to/agents

# Use module syntax
uv run python -m agents.main
```

---

## 📋 CI/CD

### GitHub Actions Workflow

**File:** `.github/workflows/phase1-backend-tests.yml`

**Triggers:**
- Push to `main` or `phase-1-*` branches
- Pull requests to `main`
- Changes in `agents/` directory

**Jobs:**
1. Install Python 3.13 and uv
2. Install dependencies with caching
3. Run ruff formatting check
4. Run ruff linting
5. Test dependency imports
6. Test configuration loading
7. Test FastAPI app import
8. Run automated test suite
9. Upload test results as artifacts

---

## 🐛 Debugging

### Enable Debug Logging

```bash
# Set in .env
LOG_LEVEL=DEBUG

# Or via environment variable
LOG_LEVEL=DEBUG make run-api
```

### View Logs

```bash
# Server logs printed to console
make run-api

# Check specific component logs
uv run python -c "from agents.agent import get_agent; get_agent()"
```

### Test Individual Components

```bash
# Test configuration
uv run python -c "from agents.config import get_settings; print(get_settings())"

# Test agent import
uv run python -c "from agents.agent import get_agent; agent = get_agent(); print('✓')"

# Test FastAPI app
uv run python -c "from agents import app; print(app.title)"
```

---

## 📦 Dependencies

### Core

- `fastapi>=0.109.0` - Web framework
- `uvicorn[standard]>=0.27.0` - ASGI server
- `websockets>=12.0` - WebSocket support
- `strands-agents[anthropic]>=1.55.0` - Agent framework

### Data & Config

- `pydantic>=2.0.0` - Data validation
- `pydantic-settings>=2.0.0` - Settings management
- `python-dotenv>=1.0.0` - Environment variables

### AWS

- `boto3>=1.39.0` - AWS SDK (via Strands)
- AWS Bedrock access required

### Development

- `ruff>=0.16.6` - Linting and formatting

---

## 🎯 Next Steps (Phase 2)

### NOLA-311 Integration

Phase 2 will add:
- Playwright browser automation
- QuickBase form submission
- Status page scraping
- Report tracking

**Files to be created:**
- `src/agents/integrations/nola311.py`
- `src/agents/integrations/browser.py`
- `src/agents/models/report.py`

See `intent/02_nola311_integration.md` (coming soon) for details.

---

## 📖 Documentation

- **Project Intent:** `/intent/00_project_overview.md`
- **Phase 1 Intent:** `/intent/01_fastapi_backend.md`
- **Test Results:** `PHASE1_TEST_RESULTS.md`
- **Overall Plan:** `/.claude/plans/this-project-is-to-polished-turing.md`

---

## 🤝 Contributing

### Before Committing

```bash
# Format code
make fmt

# Run tests
./tests/test_phase1.sh

# Test WebSocket
make test-chat
```

### Commit Message Format

```
<type>: <description>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

---

## 📄 License

See repository LICENSE file.

---

## 🙋 Support

For issues or questions:
1. Check troubleshooting section above
2. Review test results: `PHASE1_TEST_RESULTS.md`
3. Check GitHub issues: https://github.com/bshelling/hole-e-molie/issues

---

**Last Updated:** 2026-09-08  
**Phase 1 Status:** ✅ Complete  
**Next Phase:** Phase 2 - NOLA-311 Integration
