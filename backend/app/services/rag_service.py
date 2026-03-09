from app.services.llm_service import generate_response
from app.vectorstore.search_vector_db import search_jobs


def run_rag_pipeline(query: str) -> str:
    contexts = search_jobs(query)
    return generate_response(query=query, contexts=contexts)
