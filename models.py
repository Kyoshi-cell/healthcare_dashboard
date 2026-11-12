"""
models.py - the PatientRecord class (Module 2).

One PatientRecord object represents one row of the CSV after it has been
cleaned and converted to proper data types (dates, floats, ints).
Using a class keeps related data and behaviour together (OOP lecture).
"""

DATE_OUTPUT_FORMAT = "%d/%m/%Y"


class PatientRecord:
    """A single, validated healthcare record."""

    def __init__(self, name, age, gender, blood_type, medical_condition,
                 admission_date, doctor, hospital, insurance_provider,
                 billing_amount, room_number, admission_type,
                 discharge_date, medication, test_results):
        self.name = name
        self.age = age                          # int
        self.gender = gender
        self.blood_type = blood_type
        self.medical_condition = medical_condition
        self.admission_date = admission_date    # datetime.date
        self.doctor = doctor
        self.hospital = hospital
        self.insurance_provider = insurance_provider
        self.billing_amount = billing_amount    # float (GBP)
        self.room_number = room_number          # int
        self.admission_type = admission_type
        self.discharge_date = discharge_date    # datetime.date
        self.medication = medication
        self.test_results = test_results

    def length_of_stay(self):
        """Number of days between admission and discharge."""
        return (self.discharge_date - self.admission_date).days

    def billing_per_day(self):
        """Billing amount divided by length of stay.

        A same-day stay (0 days) is counted as 1 day so we never divide
        by zero. This is a design decision to mention in your report.
        """
        return self.billing_amount / max(self.length_of_stay(), 1)

    def to_dict(self):
        """Return the record as a dictionary with the original column
        names. Used by the exporter (Module 7)."""
        return {
            "Name": self.name,
            "Age": self.age,
            "Gender": self.gender,
            "Blood Type": self.blood_type,
            "Medical Condition": self.medical_condition,
            "Date of Admission":
                self.admission_date.strftime(DATE_OUTPUT_FORMAT),
            "Doctor": self.doctor,
            "Hospital": self.hospital,
            "Insurance Provider": self.insurance_provider,
            "Billing Amount": f"{self.billing_amount:.2f}",
            "Room Number": self.room_number,
            "Admission Type": self.admission_type,
            "Discharge Date":
                self.discharge_date.strftime(DATE_OUTPUT_FORMAT),
            "Medication": self.medication,
            "Test Results": self.test_results,
        }

    def __str__(self):
        return (f"{self.name} (age {self.age}) - {self.medical_condition}, "
                f"{self.admission_type} admission on "
                f"{self.admission_date.strftime(DATE_OUTPUT_FORMAT)}, "
                f"stay {self.length_of_stay()} day(s), "
                f"bill £{self.billing_amount:,.2f}")
