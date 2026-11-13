
from analytics import get_total_patients


def test_get_total_patients():
    records = ["Patient 1", "Patient 2", "Patient 3"]

    result = get_total_patients(records)

    assert result == 3


def test_get_total_patients_empty():
    records = []

    result = get_total_patients(records)

    assert result == 0
