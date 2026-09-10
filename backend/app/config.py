from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_api_key: str | None = Field(default=None, validation_alias="GOOGLE_API_KEY")
    github_token: str | None = Field(default=None, validation_alias="GITHUB_TOKEN")
    github_repo: str | None = Field(default=None, validation_alias="GITHUB_REPO")
    model: str = "gemini-2.5-flash"
    confidence_threshold: float = Field(default=0.5, ge=0, le=1)
    log_level: str = "INFO"
    cors_origins: list[str] = ["http://localhost:5173"]
    vector_store_path: str = "./.chroma"
    retrieval_top_k: int = Field(default=3, ge=1, le=20)
    retrieval_threshold: float = Field(default=0.15, ge=0, le=1)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def llm_configured(self) -> bool:
        return bool(self.google_api_key)

    @property
    def issues_configured(self) -> bool:
        return bool(self.github_token and self.github_repo)


@lru_cache
def get_settings() -> Settings:
    return Settings()
