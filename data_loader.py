
import csv
import io
from datetime import datetime
from pathlib import Path

from models import HealthcareRecord


REQUIRED_COLUMNS = [
    "Name",
    "Age",
    "Gender",
    "Blood Type",
    "Medical Condition",
    "Date of Admission",
    "Doctor",
    "Hospital",
    "Insurance Provider",
    "Billing Amount",
    "Room Number",
    "Admission Type",
    "Discharge Date",
    "Medication",
    "Test Results"
]

COLUMN_ALIASES = {
    "Data of Admission": "Date of Admission",
    "Date Of Admission": "Date of Admission"
}


def normalise_headers(headers):
    """Standardize CSV column headings."""
    normalised = []

    for header in headers:
        header = header.strip()
        header = COLUMN_ALIASES.get(header, header)
        normalised.append(header)

    return normalised


def parse_integer(value):
    """Convert a value into an integer, or return None if invalid."""
    if value is None or str(value).strip() == "":
        return None

    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_billing(value):
    """Convert a billing amount into a float, or return None."""
    if value is None or str(value).strip() == "":
        return None

    try:
        cleaned = str(value)
        cleaned = cleaned.replace("£", "")
        cleaned = cleaned.replace("$", "")
        cleaned = cleaned.replace("€", "")
        cleaned = cleaned.replace(",", "").strip()

        return float(cleaned)

    except (ValueError, TypeError):
        return None



def parse_date(value):
    """
    Convert supported date formats into datetime.date.

    The day/month/year format is prioritised because the
    university dataset contains dates in DD/MM/YYYY format.
    """
    if value is None or str(value).strip() == "":
        return None

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d %b %Y",
        "%B %d, %Y"
    ]

    for date_format in formats:
        try:
            return datetime.strptime(
                str(value).strip(),
                date_format
            ).date()

        except ValueError:
            continue

    return None



def load_healthcare_data(file_path):
    """
    Load and validate healthcare records from a CSV file.

    Args:
        file_path: Path to the healthcare CSV dataset.

    Returns:
        A tuple containing a list of HealthcareRecord objects
        and a list of validation warnings.

    Raises:
        FileNotFoundError: If the dataset does not exist.
        ValueError: If the CSV cannot be decoded or has invalid headers.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    records = []
    warnings = []

    # Read the CSV file as bytes
    raw_data = path.read_bytes()

    # Try common CSV encodings
    decoded_text = None

    for encoding in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            decoded_text = raw_data.decode(encoding)
            print(f"Dataset encoding detected: {encoding}")
            break

        except UnicodeDecodeError:
            continue

    if decoded_text is None:
        raise ValueError("Unable to decode the CSV file.")

    # Read the decoded CSV content
    with io.StringIO(decoded_text, newline="") as csv_file:

        reader = csv.DictReader(csv_file)

        if not reader.fieldnames:
            raise ValueError(
                "The CSV file is empty or has no headers."
            )

        headers = normalise_headers(reader.fieldnames)

        if len(headers) != len(set(headers)):
            raise ValueError("Duplicate column headings found.")

        reader.fieldnames = headers

        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in headers
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        # Process each patient record
        for row_number, row in enumerate(reader, start=2):

            age = parse_integer(row.get("Age"))
            billing = parse_billing(row.get("Billing Amount"))
            room_number = parse_integer(row.get("Room Number"))

            admission_date = parse_date(
                row.get("Date of Admission")
            )

            discharge_date = parse_date(
                row.get("Discharge Date")
            )

            # Validate age
            if age is None:
                warnings.append(
                    f"Row {row_number}: Invalid or missing age."
                )
            elif age < 0 or age > 120:
                warnings.append(
                    f"Row {row_number}: Age is outside 0-120."
                )

            # Validate billing
            if billing is None:
                warnings.append(
                    f"Row {row_number}: Invalid or missing billing amount."
                )

            # Validate room number
            if room_number is None:
                warnings.append(
                    f"Row {row_number}: Invalid or missing room number."
                )

            # Validate admission date
            if admission_date is None:
                warnings.append(
                    f"Row {row_number}: Invalid or missing admission date."
                )

            # Validate discharge date
            if (row.get("Discharge Date") or "").strip():
                if discharge_date is None:
                    warnings.append(
                        f"Row {row_number}: Invalid discharge date."
                    )

            # Check date order
            if (
                admission_date is not None
                and discharge_date is not None
                and discharge_date < admission_date
            ):
                warnings.append(
                    f"Row {row_number}: Discharge date is before admission."
                )

            # Check required text fields
            for field in [
                "Name",
                "Gender",
                "Medical Condition",
                "Hospital"
            ]:
                if not (row.get(field) or "").strip():
                    warnings.append(
                        f"Row {row_number}: Missing {field}."
                    )

            # Create healthcare record
            record = HealthcareRecord(
                name=(row.get("Name") or "").strip(),
                age=age,
                gender=(row.get("Gender") or "").strip(),
                blood_type=(row.get("Blood Type") or "").strip(),
                medical_condition=(
                    row.get("Medical Condition") or ""
                ).strip(),
                date_of_admission=admission_date,
                doctor=(row.get("Doctor") or "").strip(),
                hospital=(row.get("Hospital") or "").strip(),
                insurance_provider=(
                    row.get("Insurance Provider") or ""
                ).strip(),
                billing_amount=billing,
                room_number=room_number,
                admission_type=(
                    row.get("Admission Type") or ""
                ).strip(),
                discharge_date=discharge_date,
                medication=(row.get("Medication") or "").strip(),
                test_results=(row.get("Test Results") or "").strip()
            )

            records.append(record)

    return records, warnings


def print_data_summary(records, warnings):
    """Print a summary of the loaded healthcare dataset."""

    print("\n========== DATASET SUMMARY ==========")
    print(f"Total records loaded: {len(records)}")
    print(f"Validation warnings: {len(warnings)}")

    if warnings:
        print("\nFirst 10 warnings:")

        for warning in warnings[:10]:
            print(f"- {warning}")

    print("=====================================\n")
