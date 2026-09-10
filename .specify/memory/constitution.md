# RCA Buddy Constitution

## Core Principles

### I. Grounded Analysis
Every RCA must be based on the deterministic failure signature and attributable incident evidence when evidence is available. The model must state uncertainty plainly instead of inventing a confident cause.

### II. Contract-First Boundaries
Backend and frontend behavior is defined by the documented request, response, health, and error contracts. External providers are isolated behind protocol boundaries so local tests can use controlled doubles.

### III. Test-First Delivery
New behavior requires focused tests before implementation, followed by the full backend and frontend quality gates. Tests must cover both successful and degraded or unconfigured paths.

### IV. Secure Defaults
Secrets are backend-only configuration. Logs, error responses, client bundles, and health responses must not expose credentials or raw provider failures. User log content is not written to routine access logs.

### V. Accessible Operations
The primary RCA workflow must be keyboard-operable, screen-reader understandable, and communicate state with text as well as color. Confidence and dependency health must remain truthful and visible.

### VI. Small, Observable Changes
Prefer the simplest implementation that satisfies the contract. Preserve request correlation through `X-Request-ID`, use structured safe errors, and validate each story with its narrowest executable check before broader gates.

## Constraints

- The initial release uses FastAPI, React/Vite, Gemini, ChromaDB, and GitHub Issues.
- Webhooks, remediation, chat integrations, authentication, multi-tenancy, and non-GitHub issue providers are out of scope.
- Secrets are supplied through environment configuration and never committed.

## Development Workflow

Every story is implemented in dependency order with focused tests, backend Ruff and pytest checks, frontend ESLint, TypeScript, Vitest, and build checks. CI must run the same gates. Deviations from the feature plan are documented in the implementation record.

## Governance

This constitution governs implementation and review for RCA Buddy. Amendments require an explicit change to this file and a corresponding update to affected specifications, plans, tasks, or tests.

**Version**: 1.0.0 | **Ratified**: 2026-02-14 | **Last Amended**: 2026-02-14
