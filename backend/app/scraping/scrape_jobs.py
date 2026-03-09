import csv
from pathlib import Path


RAW_DATA_PATH = Path("backend/data/raw/jobs_raw.csv")


def scrape_jobs() -> Path:
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "title": "Python Backend Developer",
            "company": "Acme",
            "location": "Remote",
            "description": "Build APIs and services.",
        },
        {
            "title": "Data Engineer",
            "company": "Globex",
            "location": "New York",
            "description": "Build ETL and analytics pipelines.",
        },
    ]

    with RAW_DATA_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["title", "company", "location", "description"],
        )
        writer.writeheader()
        writer.writerows(rows)

    return RAW_DATA_PATH
