"""
data_loader.py - loading, cleaning and validating the CSV (Module 2).

Requirement A: load the dataset, convert values to suitable data types
(including dates), identify and handle invalid or missing data, and give
clear feedback when something goes wrong.

Only modules from the assessment brief are used: csv, re, datetime.

Public functions:
    load_csv(path)      -> (valid_records, rejected_rows)
    dataset_info(recs)  -> dictionary of basic facts about the dataset
"""

import csv
import re
from datetime import datetime

from models import PatientRecord

# The file contains the pound sign, so it is NOT UTF-8 (Windows-1252).
ENCODING = "cp1252"
DATE_FORMAT = "%d/%m/%Y"

REQUIRED_COLUMNS = [
    "Name", "Age", "Gender", "Blood Type", "Medical Condition",
    "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
    "Billing Amount", "Room Number", "Admission Type", "Discharge Date",
    "Medication", "Test Results",
]

# Shown to the user so they can see how each column was converted.
COLUMN_TYPES = {
    "Name": "text", "Age": "integer", "Gender": "text",
    "Blood Type": "text", "Medical Condition": "text",
    "Date of Admission": "date", "Doctor": "text", "Hospital": "text",
    "Insurance Provider": "text", "Billing Amount": "float (GBP)",
    "Room Number": "integer", "Admission Type": "text",
    "Discharge Date": "date", "Medication": "text", "Test Results": "text",
}

# Validation rules (change these in one place if your decisions change).
MAX_AGE = 120
ALLOW_NEGATIVE_BILLING = False   # design decision: a negative bill is rejected
VALID_BLOOD_TYPES = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
VALID_ADMISSION_TYPES = {"Emergency", "Urgent", "Elective"}
VALID_TEST_RESULTS = {"Normal", "Abnormal", "Inconclusive"}


# ---------------------------------------------------------------------------
# Small parsing functions. Each converts ONE text value and raises
# ValueError with a readable message if the value is not acceptable.
# ---------------------------------------------------------------------------

def parse_money(text):
    """'£18,856.28' -> 18856.28   '-£502.51' -> -502.51"""
    cleaned = text.strip()
    if cleaned == "":
        raise ValueError("amount is empty")

    # digits with proper thousands separators (1,234.50) or plain (1234.50)
    number = r"(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?"
    match = re.fullmatch(r"(-?)\s*£?\s*(-?)" + number, cleaned)
    if match is None:
        raise ValueError(f"'{text}' is not a valid amount")

    whole = match.group(3).replace(",", "")
    amount = round(float(whole + (match.group(4) or "")), 2)
    if match.group(1) or match.group(2):      # a minus sign was present
        amount = -amount
    return amount


def parse_date(text):
    """'31/01/2024' -> datetime.date(2024, 1, 31)"""
    try:
        return datetime.strptime(text.strip(), DATE_FORMAT).date()
    except ValueError:
        raise ValueError(f"'{text}' is not a valid dd/mm/yyyy date") from None


def parse_age(text):
    """Whole number between 0 and MAX_AGE."""
    cleaned = text.strip()
    if not re.fullmatch(r"\d{1,3}", cleaned):
        raise ValueError(f"'{text}' is not a whole number")
    age = int(cleaned)
    if age > MAX_AGE:
        raise ValueError(f"age {age} is outside the range 0-{MAX_AGE}")
    return age


def parse_room(text):
    """Positive whole number."""
    cleaned = text.strip()
    if not re.fullmatch(r"\d+", cleaned) or int(cleaned) == 0:
        raise ValueError(f"'{text}' is not a valid room number")
    return int(cleaned)


def parse_text(text):
    """Trim spaces, collapse repeated spaces, reject empty values."""
    cleaned = " ".join(text.split())
    if cleaned == "":
        raise ValueError("value is empty")
    return cleaned


def parse_name(text):
    """'LesLie TErRy' -> 'Leslie Terry'  (inconsistent capitals fixed).
    Limitation: .title() turns 'McDonald' into 'Mcdonald'."""
    return parse_text(text).title()


def parse_choice(text, allowed):
    """Value must be one of `allowed` (case-insensitive); returns the
    standard spelling."""
    cleaned = parse_text(text).title()
    if cleaned not in allowed:
        raise ValueError(f"'{text}' is not one of {sorted(allowed)}")
    return cleaned


def parse_blood_type(text):
    cleaned = parse_text(text).upper()
    if cleaned not in VALID_BLOOD_TYPES:
        raise ValueError(f"'{text}' is not a valid blood type")
    return cleaned


# ---------------------------------------------------------------------------
# Cleaning one row, and loading the whole file.
# ---------------------------------------------------------------------------

def _field(row, column, parser):
    """Run `parser` on row[column]; add the column name to any error."""
    try:
        return parser(row[column])
    except ValueError as error:
        raise ValueError(f"{column}: {error}") from None


def clean_record(row):
    """Turn one CSV row (a dict of text) into a PatientRecord.
    Raises ValueError (with the reason) if the row is invalid."""
    if None in row or any(value is None for value in row.values()):
        raise ValueError("row has the wrong number of columns")

    admission = _field(row, "Date of Admission", parse_date)
    discharge = _field(row, "Discharge Date", parse_date)
    if discharge < admission:
        raise ValueError("Discharge Date is before Date of Admission")

    billing = _field(row, "Billing Amount", parse_money)
    if billing < 0 and not ALLOW_NEGATIVE_BILLING:
        raise ValueError(f"Billing Amount: negative amount ({billing})")

    return PatientRecord(
        name=_field(row, "Name", parse_name),
        age=_field(row, "Age", parse_age),
        gender=_field(row, "Gender", lambda t: parse_text(t).title()),
        blood_type=_field(row, "Blood Type", parse_blood_type),
        medical_condition=_field(row, "Medical Condition",
                                 lambda t: parse_text(t).title()),
        admission_date=admission,
        doctor=_field(row, "Doctor", parse_text),
        hospital=_field(row, "Hospital", parse_text),
        insurance_provider=_field(row, "Insurance Provider", parse_text),
        billing_amount=billing,
        room_number=_field(row, "Room Number", parse_room),
        admission_type=_field(row, "Admission Type",
                              lambda t: parse_choice(t, VALID_ADMISSION_TYPES)),
        discharge_date=discharge,
        medication=_field(row, "Medication", parse_text),
        test_results=_field(row, "Test Results",
                            lambda t: parse_choice(t, VALID_TEST_RESULTS)),
    )


def load_csv(path):
    """Load the CSV file.

    Returns (valid_records, rejected_rows) where rejected_rows is a list
    of (line_number, reason) tuples. Line 1 is the header, so the first
    data row is line 2.

    Raises FileNotFoundError, PermissionError, UnicodeDecodeError (from
    open/read) or ValueError (empty file / missing columns). The caller
    decides how to tell the user.
    """
    valid = []
    rejected = []

    with open(path, "r", newline="", encoding=ENCODING) as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("The file is empty.")

        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise ValueError("Missing required column(s): " + ", ".join(missing))

        for line_number, row in enumerate(reader, start=2):
            try:
                valid.append(clean_record(row))
            except ValueError as error:
                rejected.append((line_number, str(error)))

    return valid, rejected


def dataset_info(records):
    """Basic facts about the loaded data (for the 'display basic
    information' part of requirement A). Returns a dictionary."""
    info = {"record_count": len(records), "column_types": COLUMN_TYPES}
    if records:
        admissions = [r.admission_date for r in records]
        ages = [r.age for r in records]
        info["first_admission"] = min(admissions)
        info["last_admission"] = max(admissions)
        info["youngest"] = min(ages)
        info["oldest"] = max(ages)
    return info
