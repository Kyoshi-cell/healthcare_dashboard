"""
main.py - entry point for the Healthcare Dashboard (CPS4003 Assessment 2).

Run this file to start the application:
    python main.py

Design note:
    main.py only decides HOW the program starts. All real work lives in
    other modules (data_loader, analytics, charts, exporter, gui), so this
    file stays short and easy to explain.

Only modules allowed by the assessment brief are used here (os).
"""

import os

import data_loader  # Module 2: load_csv(path) -> (valid_records, rejected_rows)

# Build the path to the CSV relative to THIS file, so the program works
# no matter which folder PyCharm / the terminal is running from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "healthcare_dataset.csv")


def load_data(path):
    """Load the CSV and report the outcome clearly to the user.

    Returns (valid_records, rejected_rows). If loading fails, both are
    empty lists, so the rest of the program never has to crash.
    """
    print(f"Loading data from: {path}")
    try:
        valid, rejected = data_loader.load_csv(path)
    except FileNotFoundError:
        print("Error: the data file was not found. Check the 'data' folder.")
        return [], []
    except PermissionError:
        print("Error: permission denied when opening the data file.")
        return [], []
    except UnicodeDecodeError:
        print("Error: the file encoding is not what the loader expected.")
        return [], []
    except ValueError as error:      # empty file or missing columns
        print(f"Error: {error}")
        return [], []
    except OSError as error:         # e.g. the path is a folder
        print(f"Error: could not read the file ({error}).")
        return [], []

    print(f"Loaded {len(valid)} valid record(s); {len(rejected)} rejected.")
    show_info(valid)
    return valid, rejected


def show_info(records):
    """Print basic information about the loaded dataset (requirement A)."""
    info = data_loader.dataset_info(records)
    print(f"  Records: {info['record_count']}")
    if records:
        print(f"  Admissions: {info['first_admission']} to "
              f"{info['last_admission']}")
        print(f"  Ages: {info['youngest']} to {info['oldest']}")
    print("  Column types:")
    for column, kind in info["column_types"].items():
        print(f"    {column}: {kind}")


def show_rejected(rejected):
    """Print each rejected row with the reason it was rejected."""
    if not rejected:
        print("No rejected rows.")
        return
    for row_number, reason in rejected:
        print(f"  Row {row_number}: {reason}")


def run_console():
    """Simple text menu. Useful while building Modules 2-7, before the GUI
    exists, and as a fallback for testing. Add a new option here each time
    you finish an analysis module."""
    records, rejected = load_data(DATA_FILE)

    while True:
        print("\n=== Healthcare Dashboard (console) ===")
        print("1. Reload data")
        print("2. Show rejected rows")
        print("3. Start the graphical dashboard")
        # TODO (Module 3):  4. Basic statistics
        # TODO (Module 4):  5. Length of stay and billing analysis
        # TODO (Module 5):  6. Outliers / data-quality report
        # TODO (Module 7):  7. Export results
        print("0. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            records, rejected = load_data(DATA_FILE)
        elif choice == "2":
            show_rejected(rejected)
        elif choice == "3":
            if not start_gui():
                print("The GUI is not available yet (Module 8).")
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")


def start_gui():
    """Launch the Tkinter dashboard. Returns False if gui.py does not
    exist yet, so the program can fall back to the console menu."""
    try:
        import gui  # Module 8
    except ModuleNotFoundError as error:
        # Only ignore "gui.py is missing". A different missing module
        # inside gui.py is a real bug and should be raised, not hidden.
        if error.name != "gui":
            raise
        return False

    gui.launch(DATA_FILE)  # gui.py must define launch(data_file)
    return True


def main():
    """Start the GUI if it exists, otherwise use the console menu."""
    if not start_gui():
        run_console()


if __name__ == "__main__":
