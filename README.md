# RCA Buddy

RCA Buddy turns CI/CD failure logs into grounded root-cause reports, shows the incident evidence used, and offers a GitHub issue hand-off when confidence is low.

## Development

Prerequisites: Python 3.12+, Node.js 20+, and npm.

```bash
cp .env.example backend/.env
python -m venv .venv
source .venv/bin/activate
python -m pip install -e 'backend[quality,test]'
cd frontend && npm install && cd ..

# Terminal 1
cd backend && uvicorn app.main:app --reload
# Terminal 2
cd frontend && npm run dev
```

Open `http://localhost:5173`. Backend API and health endpoints are available at `http://localhost:8000`.

## Quality gates

```bash
cd backend && ruff check . && ruff format --check . && pytest
cd frontend && npm run lint && npx tsc --noEmit && npm test && npm run build
```

## Production

Build the frontend, then serve the generated application through FastAPI:

```bash
cd frontend && npm run build
cd ../backend && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000`.

## Configuration

Copy `.env.example` to `backend/.env`. Google and GitHub credentials are optional for local health and UI work, and must never be committed. See `quickstart.md` for the development, production, and container walkthroughs.
