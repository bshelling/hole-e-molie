"""Tests for Phase 2 report models"""

import sys
from datetime import datetime


def test_location_model():
    """Test Location model"""
    from agents.models import Location

    # Valid location
    loc = Location(address="1234 Magazine St, New Orleans, LA")
    assert loc.address == "1234 Magazine St, New Orleans, LA"
    print("✓ Location model: basic creation")

    # Location with coordinates
    loc_with_coords = Location(
        address="1234 Magazine St",
        coordinates={'lat': 29.9311, 'lng': -90.0852}
    )
    assert loc_with_coords.coordinates['lat'] == 29.9311
    print("✓ Location model: with coordinates")

    # Test coordinate validation (should fail for coordinates outside NOLA)
    try:
        invalid_loc = Location(
            address="123 Main St",
            coordinates={'lat': 40.7128, 'lng': -74.0060}  # NYC coordinates
        )
        print("✗ Location model: should have rejected NYC coordinates")
        return False
    except ValueError:
        print("✓ Location model: coordinate validation")

    return True


def test_pothole_report_model():
    """Test PotholeReport model"""
    from agents.models import PotholeReport, Location

    loc = Location(address="1234 Magazine St, New Orleans, LA")

    # Valid report
    report = PotholeReport(
        location=loc,
        description="Large pothole in right lane, approximately 2 feet wide",
        severity="high",
        reporter_name="Jane Doe",
        email="jane@example.com",
        phone="504-555-1234"
    )
    assert report.reporter_name == "Jane Doe"
    assert report.phone == "(504) 555-1234"  # Should be formatted
    assert report.severity == "high"
    print("✓ PotholeReport model: basic creation")

    # Test phone formatting
    report2 = PotholeReport(
        location=loc,
        description="Another pothole here that needs attention",
        reporter_name="John Smith",
        email="john@example.com",
        phone="5045551234"  # No formatting
    )
    assert report2.phone == "(504) 555-1234"  # Should be auto-formatted
    print("✓ PotholeReport model: phone formatting")

    # Test email validation (should fail for invalid email)
    try:
        invalid_report = PotholeReport(
            location=loc,
            description="Test pothole description here",
            reporter_name="Test User",
            email="notanemail",  # Invalid
            phone="504-555-1234"
        )
        print("✗ PotholeReport model: should have rejected invalid email")
        return False
    except ValueError:
        print("✓ PotholeReport model: email validation")

    # Test description length validation
    try:
        short_desc_report = PotholeReport(
            location=loc,
            description="short",  # Too short
            reporter_name="Test User",
            email="test@example.com"
        )
        print("✗ PotholeReport model: should have rejected short description")
        return False
    except ValueError:
        print("✓ PotholeReport model: description length validation")

    return True


def test_status_result_model():
    """Test StatusResult model"""
    from agents.models import StatusResult

    # Valid status result
    status = StatusResult(
        reference_number="311-2026-0908-001",
        status="in_progress",
        raw_status="Assigned",
        notes="Crew assigned for repair"
    )
    assert status.reference_number == "311-2026-0908-001"
    assert status.status == "in_progress"
    assert status.raw_status == "Assigned"
    print("✓ StatusResult model: basic creation")

    # Test all status types
    for status_type in ["submitted", "in_progress", "resolved", "duplicate", "closed", "unknown"]:
        s = StatusResult(
            reference_number="311-TEST",
            status=status_type,
            raw_status="Test"
        )
        assert s.status == status_type
    print("✓ StatusResult model: all status types")

    return True


def test_submission_result_model():
    """Test SubmissionResult model"""
    from agents.models import SubmissionResult

    # Successful submission
    success_result = SubmissionResult(
        success=True,
        reference_number="311-2026-0908-001"
    )
    assert success_result.success is True
    assert success_result.reference_number == "311-2026-0908-001"
    assert success_result.error_message is None
    print("✓ SubmissionResult model: successful submission")

    # Failed submission
    failure_result = SubmissionResult(
        success=False,
        error_message="Network timeout"
    )
    assert failure_result.success is False
    assert failure_result.reference_number is None
    assert failure_result.error_message == "Network timeout"
    print("✓ SubmissionResult model: failed submission")

    return True


def run_all_tests():
    """Run all model tests"""
    print("=" * 80)
    print("Phase 2 Model Tests")
    print("=" * 80)
    print()

    tests = [
        ("Location Model", test_location_model),
        ("PotholeReport Model", test_pothole_report_model),
        ("StatusResult Model", test_status_result_model),
        ("SubmissionResult Model", test_submission_result_model),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        try:
            if test_func():
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

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
