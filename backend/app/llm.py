import json
from typing import Protocol

from .errors import NotConfiguredError, ProviderError, RateLimitedError
from .schemas import RcaReport

SYSTEM_PROMPT = """You are RCA Buddy, a CI/CD incident analyst.
Use the SIMILAR INCIDENTS below as grounding context if relevant.
Analyze the ERROR SIGNATURE and produce a structured RCA:
Return ONLY valid JSON with exactly these fields: root_cause, component, confidence, \
suggested_fix. Do not use markdown or code fences.
root cause, affected component, confidence (0-1), suggested fix.
If nothing in the context or your knowledge supports a confident answer,
set confidence below 0.5 and say so plainly rather than guessing.

SIMILAR INCIDENTS:
{context}

ERROR SIGNATURE:
{error_signature}"""


class LLMClient(Protocol):
    def analyze(self, context: str, error_signature: str) -> RcaReport: ...


class GeminiClient:
    def __init__(self, api_key: str | None, model: str):
        self.model = model
        self._client = None
        if api_key:
            try:
                from google import genai

                self._client = genai.Client(api_key=api_key)
            except Exception:
                self._client = None

    def analyze(self, context: str, error_signature: str) -> RcaReport:
        if self._client is None:
            raise NotConfiguredError("LLM_NOT_CONFIGURED")
        prompt = SYSTEM_PROMPT.format(context=context or "(none)", error_signature=error_signature)
        try:
            response = self._client.models.generate_content(model=self.model, contents=prompt)
            raw = getattr(response, "text", "")
            data = json.loads(raw[raw.find("{") : raw.rfind("}") + 1])
            return RcaReport(**data)
        except Exception as exc:
            status = getattr(exc, "status_code", None) or getattr(exc, "code", None)
            if status == 429:
                raise RateLimitedError(getattr(exc, "retry_after", None)) from exc
            print(f"LLM ERROR: {type(exc).__name__}: {exc}")
            raise ProviderError() from exc
