from fastapi import APIRouter, Request

from ..schemas import HealthResponse

router = APIRouter()


@router.get("/api/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    settings = request.app.state.settings
    vector_store = (
        "ok" if getattr(request.app.state, "retriever", None) is not None else "unavailable"
    )
    return HealthResponse(
        status="ok",
        model=settings.model if settings.llm_configured else "unconfigured",
        vector_store=vector_store,
        issues_configured=settings.issues_configured,
    )
