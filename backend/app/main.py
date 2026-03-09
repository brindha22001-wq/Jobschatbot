from fastapi import FastAPI

from app.api.routes import router as api_router


app = FastAPI(title="Jobs Chatbot API", version="0.1.0")
app.include_router(api_router, prefix="/api")


@app.get("/")
def root() -> dict:
    return {
        "message": "OpenCodes Jobs and Career AI Chatbot backend is running successfully.",
        "status": "ok",
    }


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
