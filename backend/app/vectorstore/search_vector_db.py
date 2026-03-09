import csv
import hashlib
import json
from pathlib import Path

import numpy as np

from app.config.settings import settings


BACKEND_ROOT = Path(__file__).resolve().parents[2]
CLEANED_DATA_PATH = BACKEND_ROOT / "data" / "cleaned" / "jobs_cleaned.csv"
RAW_DATA_PATH = BACKEND_ROOT / "data" / "raw" / "jobs_raw.csv"
VECTOR_DB_DIR = BACKEND_ROOT / "data" / "vector_db"
EMBEDDINGS_PATH = VECTOR_DB_DIR / "embeddings.npy"
INDEX_PATH = VECTOR_DB_DIR / "faiss_index" / "index.faiss"
INDEX_METADATA_PATH = VECTOR_DB_DIR / "faiss_index" / "index_metadata.json"

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


def _pick(row: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            return value
    return ""


def _summary(row: dict[str, str]) -> str:
    title = _pick(row, ["job_title", "title"])
    company = _pick(row, ["company_name", "company"])
    location = _pick(row, ["location"])
    experience = _pick(row, ["experience"])
    salary = _pick(row, ["salary"])
    return (
        f"{title} at {company} ({location})"
        + (f" | exp: {experience}" if experience else "")
        + (f" | salary: {salary}" if salary else "")
    ).strip()


def _row_text(row: dict[str, str]) -> str:
    title = _pick(row, ["job_title", "title"])
    company = _pick(row, ["company_name", "company"])
    location = _pick(row, ["location"])
    skills = _pick(row, ["skills"])
    description = _pick(row, ["job_description", "description"])
    return f"{title} {company} {location} {skills} {description}".lower()


def _load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            cleaned = {k: (v or "").strip() for k, v in row.items()}
            if any(cleaned.values()):
                rows.append(cleaned)
        return rows


def _load_active_rows() -> list[dict[str, str]]:
    cleaned = _load_rows(CLEANED_DATA_PATH)
    return cleaned if cleaned else _load_rows(RAW_DATA_PATH)


def _tokenize(text: str) -> list[str]:
    clean = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in text.lower())
    return [tok for tok in clean.split() if tok and tok not in STOPWORDS]


def _fallback_embed(query: str, dim: int = 256) -> np.ndarray:
    digest = hashlib.sha256(query.encode("utf-8")).digest()
    raw = np.frombuffer(digest * ((dim // len(digest)) + 1), dtype=np.uint8)[:dim]
    vector = raw.astype(np.float32)
    norm = np.linalg.norm(vector) or 1.0
    return (vector / norm).reshape(1, -1)


def _embed_query(query: str, dim: int = 256) -> np.ndarray:
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(settings.embedding_model)
        vector = model.encode([query], show_progress_bar=False, convert_to_numpy=True).astype(np.float32)
        norm = np.linalg.norm(vector, axis=1, keepdims=True)
        norm[norm == 0] = 1.0
        return vector / norm
    except Exception:
        return _fallback_embed(query, dim=dim)


def _keyword_search(rows: list[dict[str, str]], query: str, top_k: int) -> list[str]:
    tokens = _tokenize(query)
    expanded = set(tokens)
    for token in tokens:
        if token in CATEGORY_HINTS:
            expanded.update(CATEGORY_HINTS[token])

    if not expanded:
        return [_summary(row) for row in rows[:top_k]]

    scored: list[tuple[int, str]] = []
    seen: set[str] = set()
    for row in rows:
        haystack = _row_text(row)
        score = sum(1 for tok in expanded if tok in haystack)
        if score > 0:
            summary = _summary(row)
            if summary not in seen:
                scored.append((score, summary))
                seen.add(summary)

    if not scored:
        return [_summary(row) for row in rows[:top_k]]

    scored.sort(key=lambda x: x[0], reverse=True)
    return [summary for _, summary in scored[:top_k]]


def _vector_search(rows: list[dict[str, str]], query: str, top_k: int) -> list[str]:
    if not INDEX_PATH.exists() or not EMBEDDINGS_PATH.exists():
        return []

    dim = 256
    if INDEX_METADATA_PATH.exists():
        metadata = json.loads(INDEX_METADATA_PATH.read_text(encoding="utf-8"))
        dim = int(metadata.get("dimension", 256))

    query_vector = _embed_query(query, dim=dim)

    try:
        import faiss

        index = faiss.read_index(str(INDEX_PATH))
        _, indices = index.search(query_vector, min(top_k, len(rows)))
        hits = []
        for idx in indices[0].tolist():
            if 0 <= idx < len(rows):
                hits.append(_summary(rows[idx]))
        return [hit for i, hit in enumerate(hits) if hit and hit not in hits[:i]]
    except Exception:
        return []


def search_jobs(query: str, top_k: int = 5) -> list[str]:
    text = (query or "").strip()
    rows = _load_active_rows()
    if not rows:
        return []

    vector_hits = _vector_search(rows, text, top_k)
    if vector_hits:
        return vector_hits

    return _keyword_search(rows, text, top_k)
