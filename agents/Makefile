.PHONY: run-api run-api-dev run-agent fmt fmtrun-api install test-chat clean

# Run FastAPI server
run-api:
	uv run python -m agents.main

# Run FastAPI with uvicorn directly (alternative)
run-api-dev:
	uv run uvicorn agents.main:app --reload --port 8000

# Run original agent (legacy, for reference)
run-agent:
	BEDROCK_MODEL="us.anthropic.claude-sonnet-4-6" uv run src/agents/main.py

# Format code with ruff
fmt:
	uv run ruff format src/
	uv run ruff check --fix src/

# Format and run API
fmtrun-api: fmt run-api

# Install dependencies
install:
	uv sync

# Test WebSocket client (requires test_client.py)
test-chat:
	uv run python test_client.py

# Clean Python cache files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
