# Implementation Plan: Grounded RCA Assistant

## Technical Context

- Frontend: React and TypeScript served during development by Vite; CSS modules and `tokens.css` provide styles.
- Backend: Python 3.12 with FastAPI and uvicorn; pydantic-settings owns configuration.
- Integrations: Google AI Studio through `google-genai`; local persistent ChromaDB for incident retrieval; GitHub issue creation through `httpx`.
- Testing: pytest/httpx with LLM, retriever, and GitHub clients mocked; Vitest/Testing Library for the frontend.
- Quality: Ruff, ESLint, TypeScript checks, frontend build, and GitHub Actions CI.
- Delivery: multi-stage Docker build; backend serves the frontend build on port 8000.

## Architecture

The API is stateless. Request data is parsed, retrieved, analyzed, and returned within one request. `LogSource`, `Retriever`, `LLMClient`, and `IssueClient` are Python Protocols. Routers depend on those protocols and receive implementations through application composition. Secrets are loaded only by `backend/app/config.py`.

## Repository Layout

The implementation follows PRD §1.7 exactly: `backend/app`, `backend/app/routers`, `backend/tests`, `backend/kb/incidents`, `frontend/src`, `frontend/src/api`, `frontend/src/components`, `frontend/src/hooks`, `frontend/src/styles`, `.github/workflows`, `Dockerfile`, and `README.md`.

## Dependency Rationale

- `fastapi`, `uvicorn`: typed HTTP service and local production serving.
- `pydantic-settings`: environment-backed settings and validation.
- `google-genai`: Google AI Studio model client.
- `chromadb`: persistent local incident corpus and similarity search.
- `httpx`: async HTTP calls for the GitHub REST issue hand-off and test client support.
- `pytest`: backend unit and HTTP tests.
- `ruff`: backend lint and formatting gate.
- React, TypeScript, Vite: browser UI, static type contracts, and build.
- Vitest, Testing Library, jest-dom: frontend behavior and accessibility-oriented tests.
- ESLint: frontend lint gate.

## Boundaries

No server-side conversation state is persisted. FR-12 run auto-fetch is not implemented in Release 1. Webhooks, remediation, chat bots, dashboards, authentication, multi-tenant accounts, and non-GitHub CI providers remain out of scope.

## Constitution Check

Pre-design and post-design checks are recorded in the implementation report. The current constitution file is still a template, so the explicit constraints in the PRD and feature specification are used as the active release gates until the constitution is ratified.
