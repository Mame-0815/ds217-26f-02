#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """TODO: Return usable encounter dictionaries and the skipped-row count..
    """
    encounters = []
    skipped = 0

    with open(data_path, "r", encoding="utf-8") as file:
        rows = file.readlines()

    for row in rows[1:]:
        row = row.strip()

        if not row:
            skipped += 1
            print("Skipping a blank row.")
            continue

        fields = row.split(",")

        if len(fields) != 3:
            skipped += 1
            print(f"Skipping a row with the wrong number of fields: {row}")
            continue

        patient_id, visit_date, raw_systolic = fields

        try:
            systolic = int(raw_systolic)
        except ValueError:
            skipped += 1
            print(f"Skipping a row with a non-integer reading: {row}")
            continue

        if not 60 <= systolic <= 250:
            skipped += 1
            print(f"Skipping a row with an out-of-range reading: {row}")
            continue

        encounter = {
            "patient_id": patient_id,
            "visit_date": visit_date,
            "systolic": systolic,
        }

        encounters.append(encounter)

    return encounters, skipped
    pass


def main():
    """Write a systolic summary and a patient follow-up list."""
    encounters, skipped = read_encounters(DATA_PATH)

    readings = systolic_readings(encounters)
    average = mean_systolic(readings)

    if average is None:
        raise ValueError("No usable readings were found.")

    OUTPUT_DIR.mkdir(exist_ok=True)

    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {average:.2f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]

    report_path = OUTPUT_DIR / "vitals_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("\n".join(report_lines) + "\n")

    with open(report_path, "r", encoding="utf-8") as file:
        saved_report = file.read()

    print(saved_report, end="")

    cutoff = 140
    reason = (
        "For this exercise, I chose 140 to prioritize higher readings "
        "while keeping the callback list manageable."
    )

    followup_ids = patients_at_or_above(encounters, cutoff)

    followup_lines = [
        f"Cutoff: {cutoff} mmHg",
        f"Reason: {reason}",
    ]

    for patient_id in followup_ids:
        followup_lines.append(patient_id)

    followup_path = OUTPUT_DIR / "followup_list.txt"

    with open(followup_path, "w", encoding="utf-8") as file:
        file.write("\n".join(followup_lines) + "\n")


if __name__ == "__main__":
    main()
