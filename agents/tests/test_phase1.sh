#!/bin/bash
# Phase 1 automated test script

set -e  # Exit on error

echo "========================================="
echo "Phase 1: FastAPI Backend Foundation Tests"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Change to agents directory
cd "$(dirname "$0")/.."
echo "Working directory: $(pwd)"
echo ""

# Test 1: Dependencies
echo "[1/6] Testing dependencies..."
uv run python -c "import fastapi; import uvicorn; import websockets; from pydantic import BaseModel; from pydantic_settings import BaseSettings" && \
echo -e "${GREEN}✓ All dependencies installed${NC}" || \
{ echo -e "${RED}✗ Dependency import failed${NC}"; exit 1; }
echo ""

# Test 2: Configuration
echo "[2/6] Testing configuration..."
uv run python -c "from agents.config import get_settings; s = get_settings(); assert s.bedrock_model == 'us.anthropic.claude-sonnet-4-6'" && \
echo -e "${GREEN}✓ Configuration loads correctly${NC}" || \
{ echo -e "${RED}✗ Configuration test failed${NC}"; exit 1; }
echo ""

# Test 3: FastAPI app import
echo "[3/6] Testing FastAPI app..."
uv run python -c "from agents import app; assert app.title == 'HoleeMoly API'" && \
echo -e "${GREEN}✓ FastAPI app loads correctly${NC}" || \
{ echo -e "${RED}✗ FastAPI app import failed${NC}"; exit 1; }
echo ""

# Test 4: Start server in background
echo "[4/6] Starting API server..."
uv run uvicorn agents.main:app --host 127.0.0.1 --port 8000 --log-level error &
API_PID=$!
echo "Server PID: $API_PID"
sleep 3  # Give server time to start
echo ""

# Test 5: Health endpoint
echo "[5/6] Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/api/health)
echo "Response: $HEALTH_RESPONSE"

if echo "$HEALTH_RESPONSE" | grep -q '"status":"healthy"'; then
    echo -e "${GREEN}✓ Health endpoint working${NC}"
else
    echo -e "${RED}✗ Health endpoint failed${NC}"
    kill $API_PID
    exit 1
fi
echo ""

# Test 6: Config endpoint
echo "[6/6] Testing config endpoint..."
CONFIG_RESPONSE=$(curl -s http://localhost:8000/api/config)
echo "Response: $CONFIG_RESPONSE"

if echo "$CONFIG_RESPONSE" | grep -q '"model":"us.anthropic.claude-sonnet-4-6"'; then
    echo -e "${GREEN}✓ Config endpoint working${NC}"
else
    echo -e "${RED}✗ Config endpoint failed${NC}"
    kill $API_PID
    exit 1
fi
echo ""

# Cleanup
echo "Stopping server..."
kill $API_PID
wait $API_PID 2>/dev/null || true
echo ""

echo "========================================="
echo -e "${GREEN}All Phase 1 tests passed! ✓${NC}"
echo "========================================="
echo ""
echo "Manual WebSocket test:"
echo "  1. Start server: make run-api"
echo "  2. Test WebSocket: make test-chat"
echo ""
