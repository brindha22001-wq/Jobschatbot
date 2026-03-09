import json
from pathlib import Path


EMBEDDINGS_PATH = Path("backend/data/vector_db/embeddings.json")


def create_embeddings() -> Path:
    EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"vectors": [], "model": "placeholder"}
    EMBEDDINGS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return EMBEDDINGS_PATH
