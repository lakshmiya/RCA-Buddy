from typing import Protocol


class LogSource(Protocol):
    def get_log(self, log_text: str | None, source_url: str | None) -> str: ...


class PastedLogSource:
    def get_log(self, log_text: str | None, source_url: str | None) -> str:
        return (log_text or "").strip()


class GitHubActionsLogSource:
    def get_log(self, log_text: str | None, source_url: str | None) -> str:
        raise NotImplementedError("GitHub Actions run fetching is planned for Release 1.1")
