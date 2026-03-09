from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import run_rag_pipeline


router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
def chat(request: ChatRequest) -> dict:
    answer = run_rag_pipeline(request.query)
    return {"query": request.query, "answer": answer}
