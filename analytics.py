
"""
Healthcare Dashboard Analytics Module.

Contains functions for analysing healthcare records.
"""


def get_total_patients(records):
    """
    Calculate the total number of patient records.

    Args:
        records: A list of HealthcareRecord objects.

    Returns:
        int: Total number of patient records.
    """
    return len(records)
