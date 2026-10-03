"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """return a list of every encounter's systolic reading."""
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings
    pass


def mean_systolic(readings):
    """Return the mean reading, or None when the list is empty."""
    if not readings:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return the number of distinct patients in usable encounters."""
    patient_ids = set()
    for encounter in encounters:
        patient_ids.add(encounter["patient_id"])
    return len(patient_ids)
    pass


def patients_at_or_above(encounters, cutoff):
    """"Return sorted unique IDs with a reading at or above the cutoff."""
    patient_ids = set()
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            patient_ids.add(encounter["patient_id"])
    return sorted(patient_ids)
    pass
