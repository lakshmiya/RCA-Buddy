# RCA Buddy Quickstart

## Development mode

1. Copy `backend/.env.example` to `backend/.env` and set `GOOGLE_API_KEY`; set GitHub values only for issue hand-off.
2. Install backend dependencies and run `uvicorn app.main:app --reload --port 8000` from `backend`.
3. Install frontend dependencies and run `npm run dev` from `frontend`.
4. Paste a failed `pytest` log with `ImportError`; verify the RCA, confidence, suggested fix, and missing-dependency incident.
5. Paste an ambiguous log; verify low confidence and `File a GitHub issue`.
6. File the issue and verify its URL.
7. Stop the backend, submit again, select Retry after restart, and verify no retyping.
8. Verify the header health statuses.

## Production mode

1. Build the frontend with `npm run build`.
2. Start the backend without reload on port 8000.
3. Open `/`, run the same walkthrough, and verify static frontend serving.

## Container mode

1. Build with `docker build -t rca-buddy .`.
2. Run with `docker run --env-file backend/.env -p 8000:8000 rca-buddy`.
3. Open `http://localhost:8000` and repeat the walkthrough.
4. Run backend and frontend quality gates before merge.
