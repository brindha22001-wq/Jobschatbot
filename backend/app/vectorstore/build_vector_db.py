import json
from pathlib import Path

import numpy as np


BACKEND_ROOT = Path(__file__).resolve().parents[2]
VECTOR_DB_DIR = BACKEND_ROOT / "data" / "vector_db"
EMBEDDINGS_PATH = VECTOR_DB_DIR / "embeddings.npy"
METADATA_PATH = VECTOR_DB_DIR / "embeddings_metadata.json"
INDEX_PATH = VECTOR_DB_DIR / "faiss_index" / "index.faiss"
INDEX_METADATA_PATH = VECTOR_DB_DIR / "faiss_index" / "index_metadata.json"


def build_vector_db() -> Path:
    if not EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(f"Embeddings file not found: {EMBEDDINGS_PATH}")

    vectors = np.load(EMBEDDINGS_PATH).astype(np.float32)
    index_dir = INDEX_PATH.parent
    index_dir.mkdir(parents=True, exist_ok=True)

    try:
        import faiss

        dim = vectors.shape[1] if vectors.ndim == 2 and vectors.size else 256
        index = faiss.IndexFlatIP(dim)
        if vectors.size:
            index.add(vectors)
        faiss.write_index(index, str(INDEX_PATH))
        backend = "faiss"
    except Exception:
        # If faiss is unavailable, persist vectors in numpy for fallback retrieval.
        np.save(index_dir / "index_fallback.npy", vectors)
        backend = "numpy-fallback"

    embedding_meta = {}
    if METADATA_PATH.exists():
        embedding_meta = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

    INDEX_METADATA_PATH.write_text(
        json.dumps(
            {
                "backend": backend,
                "count": int(vectors.shape[0]) if vectors.ndim == 2 else 0,
                "dimension": int(vectors.shape[1]) if vectors.ndim == 2 and vectors.size else 256,
                "embedding_source": embedding_meta.get("source", ""),
                "embedding_model": embedding_meta.get("model", ""),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return INDEX_PATH
