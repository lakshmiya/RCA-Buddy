# RCA Buddy Implementation Tasks

**Feature**: Grounded RCA Assistant
**Feature directory**: `specs/001-grounded-rca-assistant`
**Source requirements**: `spec.md`, `docs/prd.md` §1.8, and the `/speckit.tasks` technical brief

> `plan.md`, `data-model.md`, `contracts/`, `research.md`, and `quickstart.md` were not present when this task list was generated. The tasks below use the explicit technical decisions in the request and PRD layout as the governing design input. The constitution file is still an unfilled template, so no enforceable project-specific constitution articles were available for this check.

## Phase 1: Setup

**Purpose**: Establish the repository layout, dependency metadata, development commands, and configuration examples required by all stories.

- [ ] T001 [P] Create backend package markers in `backend/app/__init__.py` and `backend/app/routers/__init__.py` (FR-001, FR-017)
- [ ] T002 [P] Create backend dependency, Ruff, and pytest configuration in `backend/pyproject.toml` for Python 3.12, FastAPI, uvicorn, pydantic-settings, google-genai, chromadb, PyGithub or httpx, pytest, and httpx (FR-001, FR-016, FR-017)
- [ ] T003 [P] Create frontend dependency and script metadata in `frontend/package.json` for React, TypeScript, Vite, Vitest, Testing Library, and ESLint (FR-001, FR-014, FR-015, FR-017)
- [ ] T004 [P] Create frontend compiler configuration in `frontend/tsconfig.json` with strict type checking (FR-001, FR-014, FR-017)
- [ ] T005 [P] Create frontend lint configuration in `frontend/eslint.config.js` covering TypeScript, React, hooks, and test files (FR-014, FR-015, FR-017)
- [ ] T006 [P] Create Vite and Vitest configuration with the development proxy in `frontend/vite.config.ts` (FR-001, FR-010, FR-017)
- [ ] T007 [P] Create environment configuration documentation in `.env.example` for `GOOGLE_API_KEY`, `GITHUB_TOKEN`, `GITHUB_REPO`, `MODEL`, `CONFIDENCE_THRESHOLD`, `LOG_LEVEL`, and `CORS_ORIGINS` without sample secrets (FR-008, FR-009, FR-012, FR-016)
- [ ] T008 [P] Create the initial project usage and development command skeleton in `README.md` (FR-017, FR-018)

## Phase 2: Foundational

**Purpose**: Build shared contracts, configuration, error handling, request correlation, public schemas, client types, fetch behavior, visual tokens, and seeded evidence needed by all user stories.

- [ ] T009 [P] Define typed application settings and safe defaults in `backend/app/config.py`, including model selection, confidence threshold, CORS origins, repository, and secret presence checks (FR-008, FR-009, FR-012, FR-016)
- [ ] T010 [P] Define structured logging and request-ID middleware in `backend/app/logging.py`, ensuring request IDs are generated, propagated, and excluded from sensitive request bodies (FR-016, FR-017)
- [ ] T011 [P] Define the structured error envelope and exception mappings in `backend/app/errors.py`, including validation, rate-limit retry hints, unconfigured dependencies, provider failures, and safe client messages without raw stack traces (FR-009, FR-016)
- [ ] T012 [P] Define request, response, health, error, incident, and issue schemas in `backend/app/schemas.py` matching the PRD §1.9 contracts verbatim and enforcing confidence values from 0 to 1 (FR-001, FR-004, FR-008, FR-009, FR-012, FR-013)
- [ ] T013 Wire application creation, middleware, exception handlers, and routers in `backend/app/main.py`, including a health-capable application when model or issue configuration is absent (FR-008, FR-009, FR-012, FR-016, FR-017)
- [ ] T014 [P] Mirror public backend schemas in `frontend/src/types.ts`, including RCA request/report, similar incidents, issue result, health status, and error envelope types (FR-001, FR-004, FR-008, FR-009, FR-012)
- [ ] T015 [P] Implement the typed fetch layer and `ApiError` in `frontend/src/api/client.ts`, preserving structured error codes, request IDs, retry-after hints, and original request data for callers (FR-009, FR-010, FR-011, FR-016)
- [ ] T016 [P] Define shared visual tokens and accessibility-conscious colour variables in `frontend/src/styles/tokens.css` for confidence, health, errors, focus, and AA contrast states (FR-014, FR-015)
- [ ] T017 [P] Add the missing-dependency incident write-up at `backend/kb/incidents/missing-dependency.md` with title, failure signature, cause, fix, and tags (FR-002, FR-003, FR-005)
- [ ] T018 [P] Add the flaky-test-timeout incident write-up at `backend/kb/incidents/flaky-test-timeout.md` with title, failure signature, cause, fix, and tags (FR-002, FR-003, FR-005)
- [ ] T019 [P] Add the Docker-build-OOM incident write-up at `backend/kb/incidents/docker-build-oom.md` with title, failure signature, cause, fix, and tags (FR-002, FR-003, FR-005)
- [ ] T020 [P] Add the environment-variable-misconfiguration incident write-up at `backend/kb/incidents/env-var-misconfig.md` with title, failure signature, cause, fix, and tags (FR-002, FR-003, FR-005)
- [ ] T021 [P] Add the dependency-version-conflict incident write-up at `backend/kb/incidents/dependency-version-conflict.md` with title, failure signature, cause, fix, and tags (FR-002, FR-003, FR-005)

## Phase 3: User Story 1 - Grounded RCA (P1)

**Goal**: Turn pasted failure logs into attributable RCA reports.

**Independent test**: Submit a recognizable failed log and verify deterministic signature extraction, matching incidents, root cause, component, confidence, suggested fix, and displayed evidence.

- [ ] T028 [US1] Implement deterministic failure-signature extraction in `backend/app/parsing.py` as a pure function with no model call (FR-001, FR-002)
- [x] T029 [US1] Implement ChromaDB corpus loading, embedding, top-k retrieval, similarity threshold filtering, and empty-result behavior in `backend/app/retrieval.py` with `Retriever` and `VectorRetriever` (FR-003, FR-005)
- [ ] T030 [US1] Implement the named system prompt constant and structured provider error translation in `backend/app/llm.py` with `LLMClient` and `GeminiClient`, using the PRD §1.11 prompt verbatim and configurable primary/fallback model selection (FR-004, FR-006, FR-008, FR-009, FR-016)
- [ ] T031 [US1] Implement `LogSource`, `PastedLogSource`, and the `NotImplemented` `GitHubActionsLogSource` stub in `backend/app/ingestion.py` (FR-001, FR-018)
- [ ] T032 [US1] Implement the RCA orchestration and `POST /api/rca` contract in `backend/app/routers/rca.py`, composing ingestion, parsing, retrieval, model output, confidence labeling, evidence attribution, and safe errors (FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-008, FR-009, FR-016)
- [ ] T033 [US1] Implement the RCA submission hook with `submit`, `retry`, `reset`, and request preservation in `frontend/src/hooks/useRca.ts` (FR-001, FR-004, FR-010, FR-011)
- [ ] T034 [P] [US1] Implement log and source URL entry and submit controls in `frontend/src/components/LogInput.tsx` (FR-001, FR-010, FR-011, FR-014)
- [ ] T035 [P] [US1] Implement confidence value, low-confidence label, and non-colour status presentation in `frontend/src/components/ConfidenceBadge.tsx` (FR-004, FR-006, FR-015)
- [ ] T036 [P] [US1] Implement incident evidence rendering in `frontend/src/components/SimilarIncidents.tsx` (FR-005, FR-014, FR-015)
- [ ] T037 [US1] Implement the grounded RCA report view in `frontend/src/components/RcaReport.tsx` with root cause, component, suggested fix, confidence, attribution, and empty-evidence states (FR-004, FR-005, FR-006, FR-014, FR-015)

## Phase 4: User Story 2 - Low-Confidence Hand-off (P2)

**Goal**: Make uncertainty explicit and preserve the investigation when filing a GitHub issue.

**Independent test**: Submit an ambiguous log, verify low-confidence messaging and one-click hand-off, then verify the created issue URL and number.

- [ ] T038 [P] [US2] Add mocked GitHub client tests in `backend/tests/test_issues.py` covering issue payload, URL and number response, unconfigured issue creation, provider failures, rate limits, and safe errors (FR-007, FR-008, FR-009, FR-016)
- [ ] T039 [P] [US2] Add issue-dialog tests in `frontend/src/components/FileIssueDialog.test.tsx` covering one-interaction submission, log/RCA/confidence payload, success URL and number, failure state, and keyboard operation (FR-007, FR-008, FR-009, FR-014)
- [ ] T040 [US2] Implement `IssueClient` and `GitHubIssueClient` in `backend/app/issues.py`, creating an issue from log excerpt, RCA draft, and confidence and translating issue-provider errors safely (FR-008, FR-009, FR-016)
- [ ] T041 [US2] Implement `POST /api/issues` in `backend/app/routers/issues.py` with the PRD §1.9 request and response contracts and configuration/error mappings (FR-008, FR-009, FR-016)
- [ ] T042 [US2] Implement the one-interaction low-confidence hand-off dialog in `frontend/src/components/FileIssueDialog.tsx`, showing created URL and number while retaining the RCA on failure (FR-006, FR-007, FR-008, FR-009, FR-014)

## Phase 5: User Story 3 - Retry Without Retyping (P3)

**Goal**: Recover from transient failures using the exact original request.

**Independent test**: Fail a request, restore service, click Retry, and verify the report completes with no log re-entry.

- [ ] T043 [P] [US3] Extend retry behavior tests in `frontend/src/hooks/useRca.test.ts` for preserved log text, source URL, rate-limit retry hints, reset, and successful retry after failure (FR-009, FR-010, FR-011)
- [ ] T044 [P] [US3] Add inline error and retry tests in `frontend/src/components/ErrorBanner.test.tsx` covering actionable messages, Retry activation, request preservation, and no report loss (FR-009, FR-010, FR-011, FR-016)
- [ ] T045 [US3] Implement `ErrorBanner` with inline safe error messaging and Retry action in `frontend/src/components/ErrorBanner.tsx` (FR-009, FR-010, FR-011, FR-016)
- [ ] T046 [US3] Integrate `useRca` retry and `ErrorBanner` into the application shell in `frontend/src/App.tsx` and `frontend/src/main.tsx` (FR-009, FR-010, FR-011, FR-016)

## Phase 6: User Story 4 - Health Visibility (P4)

**Goal**: Show truthful model, vector-store, and issue-creation readiness in the header.

**Independent test**: Exercise ready, unavailable, unconfigured, and unknown dependency states and verify the header reports each state accurately.

- [ ] T047 [P] [US4] Add health endpoint tests in `backend/tests/test_health.py` covering the PRD §1.9 response, model status, vector-store status, issue configuration, unavailable dependencies, request ID, and no secret leakage (FR-012, FR-013, FR-016)
- [ ] T048 [P] [US4] Add health header rendering tests in `frontend/src/components/HealthStatus.test.tsx` covering ready, unavailable, unconfigured, and unknown states without colour-only meaning (FR-012, FR-013, FR-015)
- [ ] T049 [US4] Implement `GET /api/health` in `backend/app/routers/health.py`, reporting service, model, vector-store, and issue-creation status without secrets (FR-012, FR-013, FR-016)
- [ ] T050 [US4] Implement header health status presentation in `frontend/src/components/HealthStatus.tsx` and integrate it in `frontend/src/App.tsx` (FR-012, FR-013, FR-015)

## Phase 7: User Story 5 - Accessible RCA Report (P5)

**Goal**: Make the report and its actions usable by keyboard and screen-reader users with WCAG 2.1 AA contrast.

**Independent test**: Navigate and operate report controls by keyboard and screen reader, verify polite announcements and labels, and run a contrast check.

- [ ] T051 [P] [US5] Add accessibility-focused report tests in `frontend/src/components/RcaReport.accessibility.test.tsx` for `aria-live="polite"`, semantic headings, labels, focusability, keyboard activation, non-colour status text, and contrast token usage (FR-014, FR-015)
- [ ] T052 [P] [US5] Add accessibility checks for input, issue dialog, error banner, and health status in `frontend/src/components/accessibility.test.tsx` (FR-009, FR-012, FR-014, FR-015)
- [ ] T053 [US5] Add the polite report live region, semantic structure, labels, visible focus states, and keyboard interactions in `frontend/src/components/RcaReport.tsx` and `frontend/src/components/LogInput.tsx` (FR-014, FR-015)
- [ ] T054 [US5] Verify and adjust AA contrast, focus, status text, and responsive report styles in `frontend/src/styles/tokens.css` and `frontend/src/styles/report.module.css` (FR-014, FR-015)

## Phase 8: Polish and Cross-Cutting Validation

**Purpose**: Make the release reproducible, deployable, observable, and safe to operate.

- [x] T055 [P] Update the complete development, production, and container instructions in `README.md` (FR-001, FR-007, FR-010, FR-012, FR-017, FR-018)
- [x] T056 [P] Create the three-mode acceptance walkthrough in `quickstart.md`, covering the PRD §1.14 flow, prerequisites, expected outputs, retry, issue URL, health status, and test commands (FR-017)
- [x] T057 [P] Create backend and frontend quality-gate jobs plus a container-build-on-main job in `.github/workflows/ci.yml`, running pytest, Ruff, Vitest, ESLint, TypeScript checks, frontend build, and the container build (FR-014, FR-015, FR-016, FR-017)
- [x] T058 [P] Create the multi-stage production image in `Dockerfile`, building the frontend and serving `frontend/dist` through the backend on port 8000 (FR-017)
- [x] T059 [P] Implement frontend static serving and production fallback in `backend/app/main.py` for the built `frontend/dist` application (FR-017)
- [ ] T060 [P] Add end-to-end walkthrough execution coverage in `backend/tests/test_acceptance.py` for recognizable and ambiguous logs, issue hand-off, retry after service restart, health status, and production/container modes as documented in `quickstart.md` (FR-001, FR-006, FR-007, FR-010, FR-012, FR-017)
- [ ] T061 [P] Add secret and log-body leakage regression checks in `backend/tests/test_security.py` and `frontend/src/security.test.ts`, covering client bundles, logs, error responses, request IDs, and issue payload redaction rules (FR-008, FR-009, FR-016)
- [x] T062 Run the complete local quality gate from `backend/pyproject.toml`, `frontend/package.json`, and `.github/workflows/ci.yml`, then record any required fixes in the touched source files (FR-014, FR-015, FR-016, FR-017)
- [x] T063 Run the constitution check from `.specify/memory/constitution.md` against the feature specification and this task list; document the ratified constitution and any deviations (FR-001, FR-016, FR-017, FR-018)

## Dependencies and Execution Order

### Phase dependencies

- Phase 1 is required before Phase 2.
- Phase 2 is required before all user-story phases.
- US1 is the MVP and must complete before US2 because issue hand-off consumes the RCA report and preserved request.
- US3 depends on the shared API client and US1 submission flow, but can be implemented after US1 and in parallel with US2.
- US4 depends on the shared application and configuration from Phase 2 and can proceed in parallel with US2 and US3.
- US5 depends on the report and interactive components from US1-US4.
- Phase 8 depends on all user stories for end-to-end validation and deployment packaging.

### Parallel execution examples

- **Setup**: T002, T003, T004, T005, T006, T007, and T008 can run in parallel after T001.
- **Foundational**: T009-T012, T014-T016, and T017-T021 can run in parallel; T013 follows the shared backend modules.
- **US1 tests**: T022-T027 can run in parallel before T028-T037.
- **US1 implementation**: T028, T029, T030, and T031 can run in parallel; T032 follows backend services; T034-T036 can run in parallel after shared types; T033 and T037 follow their dependencies.
- **US2**: T038 and T039 can run in parallel; T040 and T041 are backend work; T042 follows the issue contract.
- **US3 and US4**: T043-T044 can run in parallel with T047-T048; their implementation tasks can proceed independently after their respective tests.
- **US5**: T051 and T052 can run in parallel before T053-T054.
- **Polish**: T055-T058 and T061 can run in parallel; T059 follows the image/static-serving contract; T060-T063 are final validation tasks.

## Implementation Strategy

1. Complete Phase 1 and Phase 2 so all shared contracts, configuration, errors, types, and incident evidence exist.
2. Deliver the MVP as US1: deterministic parsing, retrieval, structured RCA, evidence attribution, and report rendering.
3. Add US2 so uncertain analysis has an honest, actionable human hand-off.
4. Add US3 and US4 as operational workflows that preserve user input and expose dependency readiness.
5. Complete US5 before release so the primary report workflow meets accessibility requirements.
6. Finish packaging, CI, quickstart verification, static serving, and leakage checks before merge.

**Suggested MVP scope**: Phase 1, Phase 2, and Phase 3 (US1), with the acceptance and quality gates needed to demonstrate a grounded RCA locally.
