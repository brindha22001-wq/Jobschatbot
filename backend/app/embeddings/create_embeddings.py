import json
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
EMBEDDINGS_PATH = BACKEND_ROOT / "data" / "vector_db" / "embeddings.json"


def create_embeddings() -> Path:
    EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"vectors": [], "model": "placeholder"}
    EMBEDDINGS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return EMBEDDINGS_PATH
