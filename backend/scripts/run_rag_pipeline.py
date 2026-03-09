from app.embeddings.create_embeddings import create_embeddings
from app.vectorstore.build_vector_db import build_vector_db


if __name__ == "__main__":
    embeddings_path = create_embeddings()
    index_path = build_vector_db()
    print(f"Embeddings saved at: {embeddings_path}")
    print(f"Vector index saved at: {index_path}")
