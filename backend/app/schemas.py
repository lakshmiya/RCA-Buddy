from pydantic import BaseModel, Field, model_validator


class SimilarIncident(BaseModel):
    id: str
    title: str


class RcaRequest(BaseModel):
    log_text: str | None = None
    source_url: str | None = None

    @model_validator(mode="after")
    def has_input(self) -> "RcaRequest":
        if not (self.log_text and self.log_text.strip()) and not (
            self.source_url and self.source_url.strip()
        ):
            raise ValueError("Provide log text or a source URL")
        return self


class RcaReport(BaseModel):
    root_cause: str
    component: str
    confidence: float = Field(ge=0, le=1)
    suggested_fix: str
    similar_incidents: list[SimilarIncident] = Field(default_factory=list)
    is_grounded: bool = False
    uncertainty_message: str | None = None


class IssueRequest(BaseModel):
    log_excerpt: str = Field(min_length=1)
    rca_draft: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)


class IssueResponse(BaseModel):
    issue_url: str
    issue_number: int


class HealthResponse(BaseModel):
    status: str
    model: str
    vector_store: str
    issues_configured: bool


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str
    retry_after: int | None = None


class ErrorEnvelope(BaseModel):
    error: ErrorDetail
