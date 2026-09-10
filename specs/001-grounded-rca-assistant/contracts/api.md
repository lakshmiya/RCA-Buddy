# API Contracts

## Health

`GET /api/health` returns `{ "status": "ok", "model": "...", "vector_store": "ok", "issues_configured": true }`.

## RCA

`POST /api/rca` accepts `{ "log_text": "...", "source_url": "..." | null }` and returns `{ "root_cause": "...", "component": "...", "confidence": 0.82, "suggested_fix": "...", "similar_incidents": [{ "id": "...", "title": "..." }] }`.

## Issues

`POST /api/issues` accepts `{ "log_excerpt": "...", "rca_draft": "...", "confidence": 0.41 }` and returns `{ "issue_url": "...", "issue_number": 142 }`.

## Errors

Non-success responses use `{ "error": { "code": "...", "message": "...", "request_id": "..." } }`; rate-limited responses may include `retry_after`.
