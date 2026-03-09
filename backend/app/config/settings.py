import os


class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    environment: str = os.getenv("ENVIRONMENT", "development")


settings = Settings()
