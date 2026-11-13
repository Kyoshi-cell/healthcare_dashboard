
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class HealthcareRecord:
    """
    Represents one patient's healthcare record.

    Attributes:
        name: Patient's name.
        age: Patient's age.
        gender: Patient's gender.
        blood_type: Patient's blood type.
        medical_condition: Recorded medical condition.
        date_of_admission: Date the patient was admitted.
        doctor: Doctor responsible for the patient.
        hospital: Hospital where the patient was treated.
        insurance_provider: Patient's insurance provider.
        billing_amount: Healthcare billing amount.
        room_number: Assigned room number.
        admission_type: Type of admission.
        discharge_date: Date the patient was discharged.
        medication: Medication recorded for the patient.
        test_results: Recorded test results.
    """

    name: str
    age: Optional[int]
    gender: str
    blood_type: str
    medical_condition: str
    date_of_admission: Optional[date]
    doctor: str
    hospital: str
    insurance_provider: str
    billing_amount: Optional[float]
    room_number: Optional[int]
    admission_type: str
    discharge_date: Optional[date]
    medication: str
    test_results: str

    def to_dict(self) -> dict:
        """
        Convert the healthcare record into a dictionary.

        Returns:
            A dictionary containing all record fields.
        """
        return {
            "Name": self.name,
            "Age": self.age,
            "Gender": self.gender,
            "Blood Type": self.blood_type,
            "Medical Condition": self.medical_condition,
            "Date of Admission": self.date_of_admission,
            "Doctor": self.doctor,
            "Hospital": self.hospital,
            "Insurance Provider": self.insurance_provider,
            "Billing Amount": self.billing_amount,
            "Room Number": self.room_number,
            "Admission Type": self.admission_type,
            "Discharge Date": self.discharge_date,
            "Medication": self.medication,
            "Test Results": self.test_results
        }
