import csv
from pathlib import Path


CLEANED_DATA_PATH = Path("backend/data/cleaned/jobs_cleaned.csv")


def search_jobs(query: str) -> list[str]:
    if not CLEANED_DATA_PATH.exists():
        return []

    matches: list[str] = []
    with CLEANED_DATA_PATH.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            summary = f"{row.get('title', '')} at {row.get('company', '')} ({row.get('location', '')})"
            if query.lower() in summary.lower() or query.lower() in row.get("description", "").lower():
                matches.append(summary)

    return matches[:5]
