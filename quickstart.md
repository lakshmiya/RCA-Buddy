# Quickstart

## Development mode

1. Copy `.env.example` to `backend/.env` and add provider credentials only when RCA generation or GitHub issue creation is needed.
2. Install backend and frontend dependencies as shown in `README.md`.
3. Run `uvicorn app.main:app --reload` from `backend` and `npm run dev` from `frontend`.
4. Open `http://localhost:5173`, submit a recognizable failed log, and confirm the report includes confidence and similar incidents.
5. Submit an ambiguous log and confirm the low-confidence hand-off is explicit. Without GitHub configuration, the issue action returns a safe unconfigured error.
6. Confirm the header reports model, vector store, and issue readiness.
7. Run the local quality gates from `README.md`.

## Production mode

1. Run `npm run build` from `frontend`.
2. Run `uvicorn app.main:app --host 0.0.0.0 --port 8000` from `backend`.
3. Open `http://localhost:8000` and repeat the health and RCA flow. FastAPI serves `frontend/dist` and `/api` routes from the same origin.

## Container mode

```bash
docker build -t rca-buddy .
docker run --rm -p 8000:8000 --env-file backend/.env rca-buddy
```

Open `http://localhost:8000`. The image builds the React bundle and runs the FastAPI server on port 8000.
