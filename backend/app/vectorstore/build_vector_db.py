from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = BACKEND_ROOT / "data" / "vector_db" / "faiss_index" / "index.bin"


def build_vector_db() -> Path:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_bytes(b"PLACEHOLDER_INDEX")
    return INDEX_PATH
