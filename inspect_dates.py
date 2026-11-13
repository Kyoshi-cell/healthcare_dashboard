
import csv
from pathlib import Path

from data_loader import parse_date

dataset_path = Path(__file__).parent / "data" / "healthcare_dataset.csv"

with dataset_path.open(
    "r",
    encoding="cp1252",
    newline=""
) as file:

    reader = csv.DictReader(file)

    print("DATE VALIDATION INVESTIGATION")
    print("=" * 60)

    count = 0

    for row_number, row in enumerate(reader, start=2):

        admission = parse_date(row.get("Date of Admission"))
        discharge = parse_date(row.get("Discharge Date"))

        if (
            admission is not None
            and discharge is not None
            and discharge < admission
        ):
            count += 1

            print(f"\nCSV row: {row_number}")
            print(f"Patient: {row.get('Name')}")
            print(f"Raw admission date: {row.get('Date of Admission')}")
            print(f"Raw discharge date: {row.get('Discharge Date')}")
            print(f"Parsed admission: {admission}")
            print(f"Parsed discharge: {discharge}")

            if count == 10:
                break

    print("\n" + "=" * 60)
    print(f"First problematic records inspected: {count}")
