import csv
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
CLEANED_DATA_PATH = BACKEND_ROOT / "data" / "cleaned" / "jobs_cleaned.csv"
RAW_DATA_PATH = BACKEND_ROOT / "data" / "raw" / "jobs_raw.csv"

STOPWORDS = {
    "job",
    "jobs",
    "career",
    "careers",
    "role",
    "roles",
    "opportunity",
    "opportunities",
    "in",
    "for",
    "at",
    "the",
    "a",
    "an",
}

CATEGORY_HINTS = {
    "engineering": {"engineer", "developer", "architect", "devops", "qa"},
    "it": {"developer", "engineer", "analyst", "cloud", "devops", "data"},
    "healthcare": {"nurse", "pharmacist", "lab", "doctor", "therapist"},
    "finance": {"accountant", "finance", "auditor", "analyst", "bank"},
    "design": {"designer", "ui", "ux", "graphic"},
}


def _load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    rows: list[dict[str, str]] = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cleaned_row = {key: (value or "").strip() for key, value in row.items()}
            if any(cleaned_row.values()):
                rows.append(cleaned_row)
    return rows


def _pick(row: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        value = row.get(key, "").strip()
        if value:
            return value
    return ""


def _summary(row: dict[str, str]) -> str:
    title = _pick(row, ["title", "job_title"])
    company = _pick(row, ["company", "company_name"])
    location = _pick(row, ["location"])
    return f"{title} at {company} ({location})".strip()


def _tokens(text: str) -> list[str]:
    clean = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in text.lower())
    return [tok for tok in clean.split() if tok and tok not in STOPWORDS]


def search_jobs(query: str) -> list[str]:
    query_clean = (query or "").strip().lower()
    cleaned_rows = _load_rows(CLEANED_DATA_PATH)
    rows = cleaned_rows if cleaned_rows else _load_rows(RAW_DATA_PATH)

    if not rows:
        return []

    if query_clean in {"hi", "hello", "hey", "hii", "yo"}:
        return [_summary(row) for row in rows[:5]]

    query_tokens = _tokens(query_clean)
    if not query_tokens:
        return [_summary(row) for row in rows[:5]]

    expanded_tokens = set(query_tokens)
    for token in query_tokens:
        if token in CATEGORY_HINTS:
            expanded_tokens.update(CATEGORY_HINTS[token])

    scored: list[tuple[int, str]] = []
    seen: set[str] = set()

    for row in rows:
        title = _pick(row, ["title", "job_title"])
        company = _pick(row, ["company", "company_name"])
        location = _pick(row, ["location"])
        description = _pick(row, ["description", "job_description"])
        skills = _pick(row, ["skills"])

        haystack = f"{title} {company} {location} {skills} {description}".lower()
        score = sum(1 for tok in expanded_tokens if tok in haystack)

        if score > 0:
            summary = _summary(row)
            if summary and summary not in seen:
                scored.append((score, summary))
                seen.add(summary)

    if not scored:
        return [_summary(row) for row in rows[:5]]

    scored.sort(key=lambda item: item[0], reverse=True)
    return [summary for _, summary in scored[:8]]
