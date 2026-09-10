from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import Settings, get_settings
from .errors import AppError, app_error_handler, unexpected_error_handler, validation_error_handler
from .issues import GitHubIssueClient
from .llm import GeminiClient
from .logging import RequestIdMiddleware
from .retrieval import VectorRetriever
from .routers import health, issues, rca


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title="RCA Buddy")
    app.state.settings = settings
    app.state.retriever = VectorRetriever(
        Path(__file__).parents[1] / "kb" / "incidents",
        settings.retrieval_threshold,
        settings.vector_store_path,
    )
    app.state.llm_client = GeminiClient(settings.google_api_key, settings.model)
    app.state.issue_client = GitHubIssueClient(settings.github_token, settings.github_repo)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=False,
    )
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unexpected_error_handler)
    app.include_router(health.router)
    app.include_router(rca.router)
    app.include_router(issues.router)
    dist = Path(__file__).parents[2] / "frontend" / "dist"
    if dist.exists():
        app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

        @app.get("/")
        async def index():
            return FileResponse(dist / "index.html")

    return app


app = create_app()
