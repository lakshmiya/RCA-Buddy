# React Development Skill

## Purpose

Provide guidance for building and maintaining the RootLens AI frontend using React, TypeScript and Vite.

## Project Context

RootLens AI is an AI-powered CI/CD incident root cause analysis application.

The frontend is responsible for:

* Incident description input
* Submitting incidents to the backend
* Displaying RCA results
* Showing probable root cause
* Showing confidence
* Showing supporting evidence
* Showing recommendations
* Showing knowledge-base sources
* Showing escalation status
* Showing API and validation errors
* Providing retry functionality
* Providing a clear human-escalation action

## Technology

Use:

* React
* TypeScript
* Vite
* Functional components
* React hooks
* Typed API interfaces
* Accessible HTML
* CSS appropriate for the project

## Development Guidelines

1. Use TypeScript for all React application code.
2. Prefer functional components.
3. Use reusable components rather than large monolithic components.
4. Keep API communication separate from UI components.
5. Define explicit TypeScript types for API requests and responses.
6. Handle loading, success, empty, error and retry states.
7. Do not expose backend secrets or Google AI Studio API keys in frontend code.
8. Do not place LLM logic directly in React components.
9. Keep the frontend independent of the LLM provider.
10. Use accessible labels and controls.
11. Provide meaningful error messages to users.
12. Avoid unnecessary global state.
13. Keep components focused on a single responsibility.
14. Do not hard-code RCA results or incident analysis.
15. Never claim that an RCA is certain when the backend reports low confidence.

## RCA Result UI

The RCA result should support:

* Root cause
* Confidence
* Evidence
* Recommendations
* Sources
* Escalation required
* Human escalation action

Use clear visual hierarchy so users can distinguish:

* What the AI believes happened
* Why it believes it happened
* What evidence supports the conclusion
* What the engineer should consider doing next
* Whether human investigation is required

## API Boundary

The frontend should communicate with the backend through typed API functions.

Example:

POST `/api/incidents/analyze`

Request:

```typescript
interface IncidentRequest {
  description: string;
}
```

Response:

```typescript
interface RCAResponse {
  root_cause: string;
  confidence: number;
  evidence: string[];
  recommendations: string[];
  sources: string[];
  escalation_required: boolean;
}
```

Do not duplicate backend RCA logic in the frontend.

## Error Handling

The UI must handle:

* Empty incident description
* Invalid request
* Backend unavailable
* Timeout
* Unexpected API response
* Low-confidence RCA
* Retrieval failure
* LLM failure

The user should receive a clear message and, where appropriate, a retry option.

## Testing

Frontend tests should cover:

* Incident submission
* Loading state
* Successful RCA display
* Evidence display
* Source display
* Low-confidence escalation
* API failure
* Retry
* Empty input validation
* Accessibility of important controls

## Security

Never:

* Put API keys in React source code
* Put secrets in `VITE_*` variables unless they are explicitly intended to be public
* Trust user input as executable code
* Automatically execute recommendations
* Implement automatic production changes from the UI

## Design Principle

The frontend is a decision-support interface.

The application recommends actions but does not autonomously modify production systems.
