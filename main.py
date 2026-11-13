
from pathlib import Path

from data_loader import load_healthcare_data, print_data_summary


def main():
    """
    Run the Healthcare Dashboard application.

    Loads the healthcare dataset and displays a data summary.
    """
    # Locate the project directory
    project_directory = Path(__file__).resolve().parent

    # Locate the healthcare CSV dataset
    dataset_path = project_directory / "data" / "healthcare_dataset.csv"

    try:
        # Load healthcare records and validation warnings
        records, warnings = load_healthcare_data(dataset_path)

        # Display application heading
        print("\n===================================")
        print("       HEALTHCARE DASHBOARD")
        print("===================================\n")

        # Display dataset summary
        print_data_summary(records, warnings)

        # Display the first healthcare record
        if records:
            print("FIRST HEALTHCARE RECORD")
            print("-----------------------")
            print(records[0].to_dict())
        else:
            print("No healthcare records were found.")

    except FileNotFoundError as error:
        print(f"File error: {error}")

    except ValueError as error:
        print(f"Dataset error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
