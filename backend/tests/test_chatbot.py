from pathlib import Path
import sys


sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_endpoint() -> None:
    response = client.post("/api/chat", json={"query": "python"})
    assert response.status_code == 200
    assert "answer" in response.json()
