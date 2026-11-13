
import csv
import pytest
from datetime import date

from data_loader import (
    load_healthcare_data,
    parse_integer,
    parse_billing,
    parse_date
)


def create_test_csv(file_path, rows=None):
    """Create a small CSV file for testing."""
    headers = [
        "Name", "Age", "Gender", "Blood Type",
        "Medical Condition", "Date of Admission",
        "Doctor", "Hospital", "Insurance Provider",
        "Billing Amount", "Room Number", "Admission Type",
        "Discharge Date", "Medication", "Test Results"
    ]

    if rows is None:
        rows = [[
            "John Smith", "35", "Male", "O+",
            "Diabetes", "2026-01-10", "Dr Brown",
            "City Hospital", "ABC Insurance",
            "1500.50", "101", "Emergency",
            "2026-01-15", "Aspirin", "Normal"
        ]]

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def test_parse_integer_valid():
    assert parse_integer("35") == 35


def test_parse_integer_invalid():
    assert parse_integer("abc") is None


def test_parse_integer_blank():
    assert parse_integer("") is None


def test_parse_billing_valid():
    assert parse_billing("1,500.50") == 1500.50


def test_parse_billing_currency():
    assert parse_billing("£1,500.50") == 1500.50


def test_parse_billing_invalid():
    assert parse_billing("unknown") is None


def test_parse_date_valid():
    assert parse_date("2026-01-10") == date(2026, 1, 10)


def test_parse_date_invalid():
    assert parse_date("not-a-date") is None


def test_load_valid_csv(tmp_path):
    csv_file = tmp_path / "test_healthcare.csv"
    create_test_csv(csv_file)

    records, warnings = load_healthcare_data(csv_file)

    assert len(records) == 1
    assert records[0].name == "John Smith"
    assert records[0].age == 35
    assert records[0].billing_amount == 1500.50
    assert warnings == []


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_healthcare_data("file_that_does_not_exist.csv")


def test_missing_required_column(tmp_path):
    csv_file = tmp_path / "incomplete.csv"

    with open(csv_file, "w", encoding="utf-8") as file:
        file.write("Name,Age,Gender\n")
        file.write("John Smith,35,Male\n")

    with pytest.raises(ValueError, match="Missing required columns"):
        load_healthcare_data(csv_file)


def test_invalid_values_are_retained_with_warnings(tmp_path):
    csv_file = tmp_path / "invalid_values.csv"

    invalid_row = [
        "John Smith", "abc", "Male", "O+",
        "Diabetes", "invalid-date", "Dr Brown",
        "City Hospital", "ABC Insurance",
        "unknown", "101", "Emergency",
        "2026-01-15", "Aspirin", "Normal"
    ]

    create_test_csv(csv_file, [invalid_row])

    records, warnings = load_healthcare_data(csv_file)

    assert len(records) == 1
    assert records[0].age is None
    assert records[0].billing_amount is None
    assert records[0].date_of_admission is None
    assert len(warnings) >= 3
