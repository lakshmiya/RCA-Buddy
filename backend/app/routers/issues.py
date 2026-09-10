from fastapi import APIRouter, Request, status

from ..schemas import IssueRequest, IssueResponse

router = APIRouter()


@router.post("/api/issues", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueRequest, request: Request) -> IssueResponse:
    return request.app.state.issue_client.create_issue(
        payload.log_excerpt, payload.rca_draft, payload.confidence
    )
