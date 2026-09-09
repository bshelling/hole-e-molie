# Intent: FastAPI Backend Foundation

## Phase

Phase 1 of 8

## Objective

Set up FastAPI server integrated with Strands SDK agent, establishing the API foundation for the pothole reporting chat interface.

## Scope

### In Scope
- FastAPI application structure with proper routing
- WebSocket endpoint for real-time chat with Strands agent
- REST endpoints for health checks and placeholder report routes
- CORS middleware for Next.js frontend integration
- Environment-based configuration management
- Strands agent wrapper for conversation handling
- Local testing and verification

### Out of Scope
- DynamoDB integration (Phase 3)
- NOLA-311 web automation (Phase 2)
- Agent tools for pothole reporting (Phase 4)
- Next.js frontend implementation (Phase 5)
- Notification system (Phase 6)
- Background polling (Phase 7)

## Technical Requirements

### Dependencies to Add
```toml
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "websockets>=12.0",
    "pydantic>=2.0.0",
    "python-multipart>=0.0.9",
    "python-dotenv>=1.0.0"
]
```

### Project Structure
```
/agents/src/agents/
├── main.py                    # FastAPI app entry point
├── config.py                  # Configuration management
├── api/
│   ├── routes/
│   │   ├── chat.py           # WebSocket chat endpoint
│   │   ├── reports.py        # Report endpoints (placeholder)
│   │   └── health.py         # Health check endpoint
│   ├── schemas/
│   │   ├── message.py        # Chat message schemas
│   │   └── report.py         # Report schemas (placeholder)
│   └── middleware/
│       └── cors.py           # CORS configuration
└── agent/
    └── conversation.py       # Strands agent wrapper
```

### API Endpoints

**WebSocket:**
- `ws://localhost:8000/api/chat` - Real-time chat with agent

**REST:**
- `GET /api/health` - Health check
- `GET /api/config` - Configuration info (non-sensitive)
- `GET /api/reports` - List reports (placeholder, returns empty array)
- `GET /api/reports/{report_id}` - Get report by ID (501 Not Implemented)
- `GET /api/reports/{report_id}/status` - Get report status (501 Not Implemented)

### Configuration

Environment variables (`.env`):
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

# Logging
LOG_LEVEL=INFO
```

## Implementation Tasks

1. **Add FastAPI Dependencies** (30 min)
   - Update `pyproject.toml`
   - Run `uv sync`

2. **Create Project Structure** (20 min)
   - Create directories and `__init__.py` files
   - Organize code by domain (api, agent, config)

3. **Configuration Management** (30 min)
   - Create `.env.example`
   - Implement `config.py` with Pydantic settings

4. **Strands Agent Wrapper** (45 min)
   - Create `ConversationAgent` class
   - Implement session-based conversation management
   - Support for streaming responses (prepared for future)

5. **API Schemas** (30 min)
   - Define Pydantic models for chat messages
   - Placeholder schemas for reports

6. **CORS Middleware** (15 min)
   - Configure CORS for Next.js frontend (localhost:3000)

7. **WebSocket Chat Endpoint** (60 min)
   - Implement WebSocket connection manager
   - Handle bidirectional communication
   - Integrate with Strands agent

8. **REST Endpoints** (45 min)
   - Health check endpoint
   - Config info endpoint
   - Placeholder report endpoints

9. **FastAPI Application** (45 min)
   - Rewrite `main.py` as FastAPI app
   - Include all routers
   - Setup middleware and lifecycle events

10. **Local Testing** (60 min)
    - Manual testing of all endpoints
    - WebSocket testing with `wscat`
    - Create test client script
    - Verify interactive docs at `/docs`

11. **Update Makefile** (15 min)
    - Add `make run-api` command
    - Add `make test-chat` command

**Total Time Estimate:** 5-6 hours

## Testing Strategy

### Manual Testing
- Start server: `make run-api`
- Test health: `curl http://localhost:8000/api/health`
- Test WebSocket: `wscat -c ws://localhost:8000/api/chat`
- Test docs: Open http://localhost:8000/docs

### Test Script
Create `test_client.py` to verify:
- WebSocket connection
- Message send/receive
- Agent response
- Session management

### Verification Checklist
- [ ] Server starts without errors
- [ ] Health endpoint returns 200
- [ ] WebSocket connects successfully
- [ ] Agent responds to messages
- [ ] CORS headers present
- [ ] Interactive docs accessible
- [ ] Logs show proper INFO messages

## Success Criteria

Phase 1 is complete when:
- [ ] All dependencies installed (`uv sync`)
- [ ] FastAPI server runs on port 8000
- [ ] WebSocket endpoint accepts connections and routes to Strands agent
- [ ] Agent responds to chat messages (even if simple responses)
- [ ] Health and config endpoints return correct data
- [ ] CORS configured for localhost:3000
- [ ] All manual tests pass
- [ ] Test client script runs successfully
- [ ] Code formatted with ruff
- [ ] Changes committed to git
- [ ] PR created for review (branch: `phase-1-fastapi-backend`)

## Integration Points

### With Existing Code
- Uses existing Strands SDK setup in `main.py`
- Uses existing AWS Bedrock configuration
- Maintains compatibility with current environment variables

### For Future Phases
- **Phase 2 (NOLA-311):** Will plug into agent tools
- **Phase 3 (DynamoDB):** Will replace placeholder report endpoints
- **Phase 4 (Agent Tools):** Will enhance conversation capabilities
- **Phase 5 (Next.js):** Frontend will connect to WebSocket endpoint

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Strands SDK streaming not working | Medium | Implement non-streaming first, add streaming later |
| WebSocket connection issues | High | Test with multiple clients, add connection retry logic |
| CORS misconfiguration | Medium | Test from Next.js early, verify headers |
| Performance with multiple connections | Low | Use ConnectionManager, implement connection limits if needed |

## Notes

- This phase focuses on API infrastructure only
- Agent responses will be simple until Phase 4 adds reporting tools
- Report endpoints return placeholders until Phase 3 adds DynamoDB
- WebSocket implementation prepared for streaming, even if not used initially
- Configuration designed to support both local and production environments

## Related Documents

- Overall Plan: `/Users/shelling/.claude/plans/this-project-is-to-polished-turing.md`
- Phase 1 Detailed Plan: `/Users/shelling/.claude/plans/phase-1-fastapi-backend.md`
- Project Overview: `/Users/shelling/Projects/holeemoly/intent/00_project_overview.md`
