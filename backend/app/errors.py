from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int, retry_after: int | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.retry_after = retry_after


class NotConfiguredError(AppError):
    def __init__(self, code: str):
        super().__init__(code, "This service is not configured for that operation.", 503)


class RateLimitedError(AppError):
    def __init__(self, retry_after: int | None = None):
        super().__init__(
            "RATE_LIMITED",
            "The provider is temporarily rate-limiting requests. Retry shortly.",
            429,
            retry_after,
        )


class ProviderError(AppError):
    def __init__(self):
        super().__init__(
            "PROVIDER_ERROR", "The upstream service could not complete the request.", 502
        )


def request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


def error_response(request: Request, error: AppError) -> JSONResponse:
    payload: dict[str, Any] = {
        "error": {"code": error.code, "message": error.message, "request_id": request_id(request)}
    }
    if error.retry_after is not None:
        payload["error"]["retry_after"] = error.retry_after
    return JSONResponse(payload, status_code=error.status_code)


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return error_response(request, exc)


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The request could not be validated.",
                "request_id": request_id(request),
            }
        },
        status_code=422,
    )


async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        {
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "The service could not complete the request.",
                "request_id": request_id(request),
            }
        },
        status_code=500,
    )
