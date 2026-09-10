from fastapi import APIRouter, Request

from ..errors import AppError
from ..ingestion import PastedLogSource
from ..parsing import extract_error_signature
from ..schemas import RcaReport, RcaRequest

router = APIRouter()


@router.post("/api/rca", response_model=RcaReport)
def create_rca(payload: RcaRequest, request: Request) -> RcaReport:
    source = PastedLogSource()
    log_text = source.get_log(payload.log_text, payload.source_url)
    if not log_text:
        raise AppError("SOURCE_NOT_AVAILABLE", "The submitted source could not be loaded.", 422)
    signature = extract_error_signature(log_text)
    retriever = request.app.state.retriever
    incidents = retriever.retrieve(signature.text)
    context = "\n".join(f"{incident.id}: {incident.title}" for incident in incidents)
    report = request.app.state.llm_client.analyze(context, signature.text)
    report.similar_incidents = incidents
    report.is_grounded = bool(incidents)
    if report.confidence < request.app.state.settings.confidence_threshold:
        report.uncertainty_message = "I'm not sure. The available evidence is low confidence."
        report.root_cause = (
            "No confident root cause could be established from the available evidence."
        )
    return report
