# Data Model

## RCA Request

- `log_text`: optional submitted CI/CD log text.
- `source_url`: optional source URL.
- At least one of `log_text` or `source_url` must be usable.
- Request data is request-scoped and retained in the browser for retry only.

## RCA Report

- `root_cause`: analysis text.
- `component`: affected component.
- `confidence`: number from 0 to 1.
- `suggested_fix`: recommended next action.
- `similar_incidents`: incidents used as evidence, possibly empty.

## Incident

A knowledge-base write-up with `id`, `title`, `failure_signature`, `root_cause`, `fix`, and `tags`. Incidents are read at startup and are not modified by requests.

## Issue

- `log_excerpt`: submitted evidence included in the hand-off.
- `rca_draft`: report draft.
- `confidence`: number from 0 to 1.
- Response contains `issue_url` and `issue_number`.

## Error Envelope

Every non-success response contains `error.code`, user-safe `error.message`, `error.request_id`, and optional `error.retry_after`.
