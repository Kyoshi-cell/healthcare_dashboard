
## 6. Automated Testing Results

Automated unit tests were executed using pytest to verify the functionality of the healthcare application.

**Command:**

```powershell
python -m pytest -v
```

**Latest test results:**

- Total tests collected: 16
- Tests passed: 16
- Tests failed: 0
- Data loader tests: 12 passed
- Model tests: 4 passed
- Execution time: 0.24 seconds
- Overall result: PASS

All 16 tests passed successfully following the date-format correction. This regression test confirmed that the existing model and data-loading functionality continued to work correctly.

**The tests covered:**

- Healthcare record creation
- Record data types
- Dictionary conversion
- Optional values
- Integer conversion
- Billing amount conversion
- Date conversion
- Valid CSV loading
- Missing dataset handling
- Missing CSV columns
- Invalid data handling

## 7. Actual Dataset Loading Test

**Test ID:** INT-01

**Feature:** Loading the university healthcare dataset

**Input:** `healthcare_dataset.csv`

**Expected result:**

The application should successfully read the CSV file, convert patient information into appropriate Python data types, validate the records, and display a dataset summary.

**Actual result:**

- Encoding detected: `cp1252`
- Healthcare records loaded: 499
- Validation warnings: 0
- First healthcare record displayed successfully.
- Date validation investigation identified and resolved the date-format parsing issue.

**Status:** PASS

**Observation:**

The dataset loaded successfully with no validation warnings after correcting the date parser to prioritise the `DD/MM/YYYY` format. The dataset contains 499 records, although the assessment brief specifies 500. The original dataset was not modified to add an extra record.

## 8. Defect and Debugging Log

### DEF-01: CSV Encoding Error

**Problem:** The application initially failed to read the healthcare CSV file because it could not decode the file using UTF-8.

**Cause:** The dataset uses Windows-1252 encoding.

**Correction:** Updated the data loader to support UTF-8-SIG, UTF-16, and cp1252 encodings.

**Retest result:** PASS. The dataset loaded successfully using cp1252.

### DEF-02: Incorrect Date Parsing

**Problem:** The application reported that some discharge dates occurred before admission dates.

**Cause:** The date parser prioritised the `MM/DD/YYYY` format instead of `DD/MM/YYYY`, resulting in incorrect interpretation of dates.

**Debugging method:** Created and ran `inspect_dates.py` to inspect the original CSV date values and compare them with the parsed dates.

**Correction:** Changed the date format priority to check `DD/MM/YYYY` before `MM/DD/YYYY`.

**Retest result:** PASS. The application now loads 499 records with zero validation warnings. The date inspection script also reports zero problematic records.
