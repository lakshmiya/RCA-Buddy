## 1. Product Requirements Document (PRD)

**RCA Buddy — CI/CD Incident RCA Assistant**
Version 1.0 · Status: approved for build

### 1.1 Overview
RCA Buddy is an internal developer-tooling assistant. A user pastes a failed CI/CD log (or points RCA Buddy at a GitHub Actions run), and the assistant returns a grounded root-cause analysis with a confidence score, drawing on a curated knowledge base of past incidents and runbooks. When it can't determine a cause, it says so and offers to open a GitHub issue for a human to investigate.

### 1.2 Goals and success measures
| Goal | Measure |
|---|---|
| Cut time-to-diagnosis for common failure classes | RCA returned in under 15s for the 5 seeded failure categories |
| Every RCA is grounded and attributable | `similar incidents` returned with every RCA that used the knowledge base |
| Clean hand-off when the assistant can't determine a cause | GitHub issue created via API with logs, RCA draft, and confidence |
| Production-quality foundation | CI green: backend tests, frontend tests, lint, type check; container image builds and runs |

### 1.3 Users and use cases
Engineers on a team with a CI/CD pipeline (GitHub Actions to start). Entry points: "the build just failed, why?", pasting a stack trace, or pointing RCA Buddy at a run URL. Users expect a fast, specific answer, not a generic "check your logs."

### 1.4 Scope of this release
**In scope: ** paste-a-log or fetch-a-run-by-URL; log parsing and error-signature extraction; grounded RCA generation; similar-incident retrieval; confidence scoring; GitHub issue creation on low confidence or user request; health reporting; error handling and retry; CI; container image.

**Out of scope (roadmap, §1.13): ** automatic pipeline listening/webhooks; auto-remediation (re-running jobs, rolling back deploys); Slack/Teams bot; multi-repo/org-wide dashboards; authentication and multi-tenant accounts; non-GitHub CI providers (GitLab CI, Jenkins) — interface is designed for it, but not built.

### 1.5 Architecture

```text
Browser — React + TypeScript (Vite)
   │ JSON over HTTP, /api/*
   ▼
FastAPI service
   ├─ ingestion   LogSource interface → PastedLogSource, GitHubActionsLogSource
   ├─ parsing     LogParser → extracts error signature, failing step, stack trace
   ├─ retrieval   Retriever interface → VectorRetriever over incidents/*.md (ChromaDB)
   ├─ llm         LLMClient interface → GeminiClient (google-genai)
   ├─ issues      IssueClient interface → GitHubIssueClient (GitHub REST API / MCP)
   └─ api         routers, validation, error envelope, request IDs
   │
   ▼
Gemini (gemini-2.5-flash) for RCA generation · ChromaDB for retrieval · GitHub API for hand-off
```

### 1.6 Design principles
- **Stateless API. ** No server-side session state; each request carries what it needs.
- **Interfaces at the seams. ** Log ingestion, retrieval, LLM access, and issue creation each sit behind a small interface with one implementation this release — so swapping GitHub Actions for GitLab CI, or Chroma for Qdrant, is a new implementation, not a rewrite.
- **Typed at every boundary. ** Pydantic models on the API; TypeScript types in the client mirror them.
- **Every RCA is attributable. ** If the knowledge base contributed to the answer, the documents used are returned and shown.
- **Fail loud, fail safe. ** Low-confidence or ungrounded RCAs are labeled as such, never presented with false certainty.

### 1.7 Repository layout

```text
rca-buddy/
├── backend/
│   ├── app/
│   │   ├── main.py               create_app(): middleware, routers, static serving
│   │   ├── config.py             Settings (pydantic-settings, .env)
│   │   ├── logging.py            structured logging, request-ID middleware
│   │   ├── errors.py             error envelope + exception handlers
│   │   ├── schemas.py            request/response models
│   │   ├── ingestion.py          LogSource protocol, PastedLogSource, GitHubActionsLogSource
│   │   ├── parsing.py            LogParser: error signature + stack trace extraction
│   │   ├── retrieval.py          Retriever protocol, VectorRetriever (ChromaDB)
│   │   ├── llm.py                LLMClient protocol, GeminiClient, RCA system prompt
│   │   ├── issues.py             IssueClient protocol, GitHubIssueClient
│   │   └── routers/
│   │       ├── health.py         GET  /api/health
│   │       ├── rca.py            POST /api/rca
│   │       └── issues.py         POST /api/issues
│   ├── kb/incidents/             seeded past-incident write-ups (.md), one per failure class
│   ├── tests/                    pytest + httpx; LLM and GitHub client mocked
│   ├── pyproject.toml
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── main.tsx  App.tsx
│   │   ├── types.ts              mirrors backend schemas
│   │   ├── api/client.ts         typed fetch layer; ApiError
│   │   ├── hooks/useRca.ts       submit log, poll/await RCA, retry
│   │   ├── components/           LogInput, RcaReport, ConfidenceBadge, SimilarIncidents, FileIssueDialog
│   │   └── styles/
│   ├── src/**/*.test.tsx
│   ├── vite.config.ts
│   └── package.json
├── .github/workflows/ci.yml
├── Dockerfile
└── README.md
```

### 1.8 Functional requirements

| ID | Requirement |
|---|---|
| FR-1 | The user can paste raw log text or a GitHub Actions run URL and submit it for analysis. |
| FR-2 | The service extracts an error signature (failing step, exception type, first/last relevant lines) from the raw log before calling the model. |
| FR-3 | The service retrieves the top-matching past incidents from the knowledge base by semantic similarity to the error signature. |
| FR-4 | The RCA response includes: probable root cause, affected component, a confidence score (0–1), a suggested fix, and the list of similar past incidents used, or an empty list if none matched. |
| FR-5 | When confidence is below a configured threshold, the assistant says it isn't sure and offers "File a GitHub issue" instead of guessing. |
| FR-6 | "File a GitHub issue" creates an issue via `POST /api/issues` containing the log excerpt, the RCA draft, and confidence; the UI shows the created issue URL. |
| FR-7 | `GET /api/health` reports service status, configured model, vector store status, and whether GitHub issue creation is configured. |
| FR-8 | If the LLM is not configured, `POST /api/rca` returns `503 LLM_NOT_CONFIGURED`; the rest of the app still runs. |
| FR-9 | If the model provider rate-limits, the service returns `429 RATE_LIMITED` with a retry-after hint; the UI offers Retry, preserving the submitted log. |
| FR-10 | Any failed request shows an inline error with Retry that resends the original input. |
| FR-11 | The RCA report view is `aria-live="polite"`; all controls are labelled and keyboard-operable; colour contrast meets WCAG AA. |
| FR-12 (stretch) | `GET /api/runs/{owner}/{repo}/{run_id}` fetches a GitHub Actions run's logs directly via the GitHub API, skipping manual paste. |

### 1.9 API

```text
GET  /api/health
     200 { "status": "ok", "model": "gemini-2.5-flash", "vector_store": "ok", "issues_configured": true }

POST /api/rca
     body { "log_text": "...", "source_url": "..." | null }
     200 { "root_cause": "...", "component": "...", "confidence": 0.82,
           "suggested_fix": "...", "similar_incidents": [{ "id": "...", "title": "..." }] }
     422 validation error   429 RATE_LIMITED   503 LLM_NOT_CONFIGURED

POST /api/issues
     body { "log_excerpt": "...", "rca_draft": "...", "confidence": 0.41 }
     201 { "issue_url": "https://github.com/.../issues/142", "issue_number": 142 }
     422 validation error   503 ISSUES_NOT_CONFIGURED

GET  /               built frontend (production mode)
```

**Error envelope.** `{ "error": { "code": "RATE_LIMITED", "message": "...", "request_id": "..." } }`.

### 1.10 Data

| Entity | Fields | Storage |
|---|---|---|
| RCA Request | `log_text`, `source_url` | Not persisted — request-scoped |
| RCA Report | `root_cause`, `component`, `confidence`, `suggested_fix`, `similar_incidents` | Not persisted — returned to client |
| Incident (knowledge base) | title, failure signature, root cause, fix, tags | `backend/kb/incidents/*.md`, embedded into ChromaDB at start-up |
| Issue | GitHub issue URL/number | GitHub, via `IssueClient` — not stored locally |

### 1.11 Model and prompt

| | Model ID | Rationale |
|---|---|---|
| Primary | `gemini-2.5-flash` | Fast, cheap, strong enough for structured log analysis |
| Fallback | `gemini-2.5-pro` | Higher quality for ambiguous, multi-cause failures |

```text
You are RCA Buddy, a CI/CD incident analyst.
Use the SIMILAR INCIDENTS below as grounding context if relevant.
Analyze the ERROR SIGNATURE and produce a structured RCA:
root cause, affected component, confidence (0-1), suggested fix.
If nothing in the context or your knowledge supports a confident answer,
set confidence below 0.5 and say so plainly rather than guessing.

SIMILAR INCIDENTS:
{context}

ERROR SIGNATURE:
{error_signature}
```

### 1.12 Non-functional requirements
**Security.** `GOOGLE_API_KEY` and `GITHUB_TOKEN` read from `backend/.env`, never reach the client. CORS allows the dev origin only. `.env` is git-ignored.
**Reliability.** Health check works even when the LLM or GitHub client is unconfigured; provider errors map to typed codes, never a raw stack trace.
**Observability.** Structured logs with request ID, method, path, status, duration.
**Quality gates.** `pytest`, `ruff check`, `ruff format --check` (backend) · `vitest`, `eslint`, `tsc --noEmit`, `vite build` (frontend) — all pass locally and in CI before merge.

### 1.13 Roadmap
| Release | Capability |
|---|---|
| 1.1 | GitHub Actions run auto-fetch (FR-12) |
| 2 | Webhook listener — auto-analyze every failed run |
| 2 | GitLab CI / Jenkins `LogSource` implementations |
| 3 | Auto-remediation suggestions with one-click re-run |
| 3 | Slack/Teams notification channel |

### 1.14 Acceptance walkthrough
1. User pastes a failed `pytest` log with an `ImportError`.
2. RCA Buddy returns: root cause "missing dependency in `requirements.txt`", component `backend/tests`, confidence 0.88, suggested fix, and one similar past incident.
3. User pastes an ambiguous log with no clear signature.
4. RCA Buddy reports low confidence (< 0.5) and offers "File a GitHub issue."
5. User clicks it; an issue is created and its URL is shown.
6. Backend is stopped; the next submit shows an error with Retry. Backend restarts; Retry succeeds.
7. Health indicator is green; CI is green; the container image runs the walkthrough.


