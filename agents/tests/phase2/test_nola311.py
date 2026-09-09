"""Tests for NOLA-311 connector (mock tests)"""

import sys
import asyncio


async def test_nola311_connector_init():
    """Test NOLA311Connector initialization"""
    from agents.integrations import NOLA311Connector

    # Test headless mode
    connector = NOLA311Connector(headless=True)
    assert connector.headless is True
    print("✓ NOLA311Connector: initialization")

    return True


async def test_status_normalization():
    """Test status normalization logic"""
    from agents.integrations.nola311 import NOLA311Connector

    connector = NOLA311Connector()

    # Test various status mappings
    test_cases = [
        ("Open", "submitted"),
        ("New", "submitted"),
        ("In Progress", "in_progress"),
        ("Assigned", "in_progress"),
        ("Closed", "resolved"),
        ("Completed", "resolved"),
        ("Duplicate", "duplicate"),
        ("Cancelled", "closed"),
        ("Unknown Status", "unknown"),
    ]

    for raw_status, expected in test_cases:
        normalized = connector._normalize_status(raw_status)
        assert normalized == expected, f"Expected {expected} for {raw_status}, got {normalized}"

    print("✓ NOLA311Connector: status normalization")
    return True


async def test_submission_result_handling():
    """Test submission result handling"""
    from agents.models import SubmissionResult

    # Test success result
    success = SubmissionResult(
        success=True,
        reference_number="311-TEST-001"
    )
    assert success.success is True
    assert success.reference_number == "311-TEST-001"

    # Test failure result
    failure = SubmissionResult(
        success=False,
        error_message="Test error"
    )
    assert failure.success is False
    assert failure.error_message == "Test error"

    print("✓ NOLA311Connector: submission result handling")
    return True


def run_all_tests():
    """Run all NOLA-311 connector tests"""
    print("=" * 80)
    print("Phase 2 NOLA-311 Connector Tests")
    print("=" * 80)
    print()

    tests = [
        ("NOLA311Connector Init", test_nola311_connector_init),
        ("Status Normalization", test_status_normalization),
        ("Submission Result Handling", test_submission_result_handling),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        try:
            result = asyncio.run(test_func())
            if result:
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                failed += 1
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"✗ {test_name} FAILED: {e}")
        print()

    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 80)
    print()
    print("Note: Full integration tests require manual form reconnaissance.")
    print("Run: uv run python scripts/explore_nola311.py")
    print()

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
