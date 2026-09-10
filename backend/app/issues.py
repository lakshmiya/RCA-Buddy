from typing import Protocol

import httpx

from .errors import NotConfiguredError, ProviderError, RateLimitedError
from .schemas import IssueResponse


class IssueClient(Protocol):
    def create_issue(
        self, log_excerpt: str, rca_draft: str, confidence: float
    ) -> IssueResponse: ...


class GitHubIssueClient:
    def __init__(self, token: str | None, repository: str | None):
        self.token = token
        self.repository = repository

    def create_issue(self, log_excerpt: str, rca_draft: str, confidence: float) -> IssueResponse:
        if not self.token or not self.repository:
            raise NotConfiguredError("ISSUES_NOT_CONFIGURED")
        owner, repo = self.repository.split("/", 1)
        payload = {
            "title": f"RCA Buddy investigation ({confidence:.2f})",
            "body": (
                f"## Log\n{log_excerpt}\n\n## RCA draft\n{rca_draft}"
                f"\n\nConfidence: {confidence:.2f}"
            ),
        }
        try:
            response = httpx.post(
                f"https://api.github.com/repos/{owner}/{repo}/issues",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/vnd.github+json",
                },
                timeout=15,
            )
            if response.status_code == 429:
                raise RateLimitedError()
            response.raise_for_status()
            data = response.json()
            return IssueResponse(issue_url=data["html_url"], issue_number=data["number"])
        except RateLimitedError:
            raise
        except Exception as exc:
            raise ProviderError() from exc
