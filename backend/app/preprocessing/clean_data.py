import csv
from pathlib import Path


RAW_DATA_PATH = Path("backend/data/raw/jobs_raw.csv")
CLEANED_DATA_PATH = Path("backend/data/cleaned/jobs_cleaned.csv")


def clean_jobs_data() -> Path:
    CLEANED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with RAW_DATA_PATH.open("r", newline="", encoding="utf-8") as src, CLEANED_DATA_PATH.open(
        "w", newline="", encoding="utf-8"
    ) as dst:
        reader = csv.DictReader(src)
        fieldnames = reader.fieldnames or ["title", "company", "location", "description"]
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            writer.writerow({key: (value or "").strip() for key, value in row.items()})

    return CLEANED_DATA_PATH
