from functools import lru_cache
from pathlib import Path
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseModel):
    app_name: str = Field(default="PocketSmart AI")
    environment: str = Field(default="development")
    secret_key: str = Field(default="dev-only-change-me")
    database_url: str = Field(default=f"sqlite:///{BASE_DIR / 'data' / 'pocketsmart.db'}")
    gemini_api_key: str = Field(default="")
    gemini_model: str = Field(default="gemini-3.8-flash")
    access_token_expire_minutes: int = Field(default=120)
    max_upload_mb: int = Field(default=5)
    cors_origins: str = Field(default="http://127.0.0.1:8000,http://localhost:8000")

    @property
    def cors_origin_list(self):
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

    @property
    def upload_dir(self):
        path = BASE_DIR / "uploads"
        path.mkdir(exist_ok=True)
        return path

@lru_cache
def get_settings():
    return Settings(
        app_name=os.getenv("APP_NAME", "PocketSmart AI"),
        environment=os.getenv("ENVIRONMENT", "development"),
        secret_key=os.getenv("SECRET_KEY", "dev-only-change-me"),
        database_url=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'data' / 'pocketsmart.db'}"),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120")),
        max_upload_mb=int(os.getenv("MAX_UPLOAD_MB", "5")),
        cors_origins=os.getenv("CORS_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000"),
    )
