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
METADATA_PATH = VECTOR_DB_DIR / "embeddings_metadata.json"


def _pick(row: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            return value
    return ""


def _load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    rows: list[dict[str, str]] = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cleaned = {k: (v or "").strip() for k, v in row.items()}
            if any(cleaned.values()):
                rows.append(cleaned)
    return rows


def _row_text(row: dict[str, str]) -> str:
    title = _pick(row, ["job_title", "title"])
    company = _pick(row, ["company_name", "company"])
    location = _pick(row, ["location"])
    experience = _pick(row, ["experience"])
    salary = _pick(row, ["salary"])
    skills = _pick(row, ["skills"])
    description = _pick(row, ["job_description", "description"])
    return (
        f"job title: {title}. company: {company}. location: {location}. "
        f"experience: {experience}. salary: {salary}. skills: {skills}. details: {description}"
    )


def _fallback_embeddings(texts: list[str], dim: int = 256) -> np.ndarray:
    vectors = np.zeros((len(texts), dim), dtype=np.float32)
    for idx, text in enumerate(texts):
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        raw = np.frombuffer(digest * ((dim // len(digest)) + 1), dtype=np.uint8)[:dim]
        vec = raw.astype(np.float32)
        norm = np.linalg.norm(vec) or 1.0
        vectors[idx] = vec / norm
    return vectors


def create_embeddings() -> Path:
    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

    rows = _load_rows(CLEANED_DATA_PATH)
    source_path = CLEANED_DATA_PATH
    if not rows:
        rows = _load_rows(RAW_DATA_PATH)
        source_path = RAW_DATA_PATH

    if not rows:
        np.save(EMBEDDINGS_PATH, np.zeros((0, 256), dtype=np.float32))
        METADATA_PATH.write_text(
            json.dumps(
                {
                    "source": str(source_path),
                    "count": 0,
                    "dimension": 256,
                    "model": settings.embedding_model,
                    "backend": "none",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return EMBEDDINGS_PATH

    texts = [_row_text(row) for row in rows]

    backend = "sentence-transformers"
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(settings.embedding_model)
        vectors = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        vectors = vectors.astype(np.float32)
    except Exception:
        backend = "fallback-hash"
        vectors = _fallback_embeddings(texts)

    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    vectors = vectors / norms

    np.save(EMBEDDINGS_PATH, vectors)
    METADATA_PATH.write_text(
        json.dumps(
            {
                "source": str(source_path),
                "count": int(vectors.shape[0]),
                "dimension": int(vectors.shape[1]),
                "model": settings.embedding_model,
                "backend": backend,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return EMBEDDINGS_PATH
