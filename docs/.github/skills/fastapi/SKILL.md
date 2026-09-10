# FastAPI Backend Development Skill

## Purpose

Provide guidance for building the RootLens AI backend using Python and FastAPI.

## Project Context

RootLens AI is an AI-powered CI/CD incident root cause analysis application.

The backend is responsible for:

* Receiving incident descriptions
* Validating requests
* Retrieving relevant knowledge
* Calling the RAG pipeline
* Calling the LLM through LangChain
* Producing structured RCA results
* Returning evidence and sources
* Determining whether escalation is required
* Creating an optional incident ticket
* Providing health status
* Handling failures safely

## Technology

Use:

* Python 3.12+
* FastAPI
* Pydantic
* Uvicorn
* LangChain
* ChromaDB
* Google AI Studio
* pytest
* httpx

FastAPI should be used as the HTTP API boundary.

## API Structure

Use a modular structure similar to:

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes/
│   ├── models/
│   ├── services/
│   │   ├── rca/
│   │   ├── rag/
│   │   └── llm/
│   └── core/
├── kb/
└── tests/
```

Keep HTTP routing separate from business logic.

## API Endpoints

Implement:

### Health

GET `/api/health`

Expected response should indicate that the backend is available.

### Analyze Incident

POST `/api/incidents/analyze`

Request:

```json
{
  "description": "Order Processing API deployment failed after the build-agent image was updated."
}
```

Response:

```json
{
  "root_cause": "Build-agent image incompatibility",
  "confidence": 0.89,
  "evidence": [],
  "recommendations": [],
  "sources": [],
  "escalation_required": false
}
```

### Ticket

POST `/api/tickets`

Creates an optional human-review incident ticket.

## Pydantic Models

Use explicit request and response models.

Example:

```python
from pydantic import BaseModel, Field


class IncidentRequest(BaseModel):
    description: str = Field(min_length=10)


class RCAResponse(BaseModel):
    root_cause: str
    confidence: float
    evidence: list[str]
    recommendations: list[str]
    sources: list[str]
    escalation_required: bool
```

Keep validation at the API boundary.

## Architecture

Use this flow:

```text
FastAPI Router
      ↓
RCA Service
      ↓
RAG Service
      ↓
ChromaDB
      ↓
Retrieved Evidence
      ↓
LangChain
      ↓
Google AI Studio
      ↓
Structured RCA
      ↓
FastAPI Response
```

The API layer must not contain the complete RAG or LLM implementation.

## Dependency Injection

Use clear service boundaries so that:

* RAG can be mocked
* LLM can be mocked
* Tests do not require live Google AI Studio calls
* ChromaDB can be replaced or isolated during tests

## Error Handling

Handle failures gracefully.

Examples:

* Invalid request → HTTP 400/422 as appropriate
* Backend dependency unavailable → appropriate 5xx response
* Retrieval failure → safe error response
* LLM failure → safe error response
* Unexpected exception → generic error without exposing internal details

Never expose:

* API keys
* Environment variables
* Stack traces to end users
* Internal filesystem paths
* Secrets

## Responsible AI

The backend must enforce these principles:

1. RCA must be grounded in retrieved knowledge.
2. Evidence must come from retrieved sources.
3. The model must not fabricate sources.
4. Confidence must be represented explicitly.
5. Low-confidence analysis should trigger human escalation.
6. The system must not automatically modify production systems.
7. LLM output must not be treated as an instruction to execute infrastructure commands.

## LLM Boundary

Keep Google AI Studio/LangChain implementation behind an LLM service interface.

Do not call the LLM directly from FastAPI route functions.

This makes it possible to mock the LLM during testing.

## RAG Boundary

Keep ChromaDB and retrieval logic behind a RAG/retriever service.

The RCA service should receive retrieved documents rather than directly managing vector database internals.

## Testing

Use pytest and httpx.

Tests should cover:

* Health endpoint
* Valid incident
* Empty incident
* Invalid incident
* Known incident
* Unknown incident
* Low-confidence response
* Escalation
* Retrieval failure
* LLM failure
* Malformed model response
* Secret protection

LLM calls must be mocked in normal unit tests.

## Security

Never:

* Hard-code API keys
* Commit `.env`
* Execute model-generated shell commands
* Execute model-generated production commands
* Automatically roll back deployments
* Automatically delete resources
* Automatically modify infrastructure

## Development Principle

FastAPI provides the API boundary.

Business logic belongs in services.

RAG belongs in the retrieval layer.

LLM interaction belongs in the LLM layer.

The system provides decision support to engineers and does not autonomously fix production incidents.
