from pathlib import Path


INDEX_PATH = Path("backend/data/vector_db/faiss_index/index.bin")


def build_vector_db() -> Path:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_bytes(b"PLACEHOLDER_INDEX")
    return INDEX_PATH
