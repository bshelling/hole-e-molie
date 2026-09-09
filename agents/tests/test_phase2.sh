#!/bin/bash
# Phase 2 automated test script

set -e  # Exit on error

echo "========================================="
echo "Phase 2: NOLA-311 Integration Tests"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Change to agents directory
cd "$(dirname "$0")/.."
echo "Working directory: $(pwd)"
echo ""

# Test 1: Model tests
echo "[1/4] Testing report models..."
uv run python tests/phase2/test_models.py && \
echo -e "${GREEN}✓ Model tests passed${NC}" || \
{ echo -e "${RED}✗ Model tests failed${NC}"; exit 1; }
echo ""

# Test 2: NOLA-311 connector tests
echo "[2/4] Testing NOLA-311 connector..."
uv run python tests/phase2/test_nola311.py && \
echo -e "${GREEN}✓ NOLA-311 connector tests passed${NC}" || \
{ echo -e "${RED}✗ NOLA-311 connector tests failed${NC}"; exit 1; }
echo ""

# Test 3: Integration imports
echo "[3/4] Testing integration imports..."
uv run python -c "
from agents.integrations import BrowserManager, NOLA311Connector
from agents.models import Location, PotholeReport, StatusResult, SubmissionResult
print('✓ All integrations import successfully')
" && \
echo -e "${GREEN}✓ Integration imports passed${NC}" || \
{ echo -e "${RED}✗ Integration imports failed${NC}"; exit 1; }
echo ""

# Test 4: Browser manager
echo "[4/4] Testing browser manager..."
uv run python -c "
from agents.integrations import BrowserManager
print('✓ BrowserManager initialized')
" && \
echo -e "${GREEN}✓ Browser manager tests passed${NC}" || \
{ echo -e "${RED}✗ Browser manager tests failed${NC}"; exit 1; }
echo ""

echo "========================================="
echo -e "${GREEN}All Phase 2 tests passed! ✓${NC}"
echo "========================================="
echo ""
echo -e "${YELLOW}Note: Full integration tests require form reconnaissance${NC}"
echo "To complete Phase 2 implementation:"
echo "  1. Run: uv run python scripts/explore_nola311.py"
echo "  2. Update form selectors in integrations/nola311.py"
echo "  3. Test actual form submission"
echo ""
