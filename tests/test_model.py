
from datetime import date

from models import HealthcareRecord


def create_sample_record():
    """Create a sample healthcare record for testing."""
    return HealthcareRecord(
        name="John Smith",
        age=35,
        gender="Male",
        blood_type="O+",
        medical_condition="Diabetes",
        date_of_admission=date(2026, 1, 10),
        doctor="Dr Brown",
        hospital="City Hospital",
        insurance_provider="ABC Insurance",
        billing_amount=1500.50,
        room_number=101,
        admission_type="Emergency",
        discharge_date=date(2026, 1, 15),
        medication="Aspirin",
        test_results="Normal"
    )


def test_record_creation():
    """Check that a record stores the correct values."""
    record = create_sample_record()

    assert record.name == "John Smith"
    assert record.age == 35
    assert record.hospital == "City Hospital"


def test_record_data_types():
    """Check that important fields use the expected data types."""
    record = create_sample_record()

    assert isinstance(record.age, int)
    assert isinstance(record.billing_amount, float)
    assert isinstance(record.date_of_admission, date)


def test_record_to_dict():
    """Check that a record can be converted into a dictionary."""
    record = create_sample_record()

    result = record.to_dict()

    assert isinstance(result, dict)
    assert result["Name"] == "John Smith"
    assert result["Age"] == 35
    assert result["Billing Amount"] == 1500.50


def test_record_allows_missing_optional_values():
    """Check that optional numeric and date fields can be None."""
    record = create_sample_record()

    record.age = None
    record.billing_amount = None
    record.date_of_admission = None

    assert record.age is None
    assert record.billing_amount is None
    assert record.date_of_admission is None
