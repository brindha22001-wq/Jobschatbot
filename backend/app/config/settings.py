import os


class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    hf_api_token: str = os.getenv("HF_API_TOKEN", "")
    hf_model: str = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    environment: str = os.getenv("ENVIRONMENT", "development")


settings = Settings()
