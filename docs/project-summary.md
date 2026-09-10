RCA Buddy – Project Summary
Project Overview

RCA Buddy is an AI-powered Root Cause Analysis (RCA) decision-support application designed to assist DevOps and application-support teams in investigating CI/CD incidents. The application combines Retrieval-Augmented Generation (RAG), a vector database, and an LLM to provide evidence-based RCA recommendations.

Problem

CI/CD incident investigation often requires engineers to review incident descriptions, troubleshooting documentation, historical knowledge, and technical evidence manually. This can increase investigation time and result in inconsistent RCA outcomes. RCA Buddy provides a structured approach to retrieve relevant knowledge and generate a concise RCA report.

Solution

The user submits an incident description through the React interface. The FastAPI backend processes the request and uses LangChain to coordinate the retrieval and LLM workflow.

Relevant information is retrieved from the Markdown-based Knowledge Base, which is indexed in ChromaDB. The retrieved context is provided to Gemini through Google AI Studio, allowing the model to generate a grounded response.

The output includes:

Probable root cause
Affected component
Confidence score
Knowledge-base sources
Recommended next steps

When sufficient evidence is not available, RCA Buddy returns a low-confidence result rather than presenting an unsupported root cause.

Architecture
User
  ↓
React + TypeScript + Vite
  ↓
FastAPI REST API
  ↓
LangChain
  ↓
ChromaDB ← Knowledge Base
  ↓
Relevant Context
  ↓
Gemini / Google AI Studio
  ↓
RCA Report
  ├── Root Cause
  ├── Component
  ├── Confidence
  ├── Sources
  └── Recommended Actions

The architecture follows a separation of responsibilities between the frontend, API layer, retrieval layer, and LLM integration.

Technology Stack
Layer	Technology
Frontend	React, TypeScript, Vite
Backend	Python, FastAPI
AI orchestration	LangChain
LLM	Gemini / Google AI Studio
Vector database	ChromaDB
Knowledge source	Markdown
Testing	pytest and frontend validation
CI/CD	GitHub Actions
AI development	GitHub Copilot + Spec Kit
Repository integration	GitHub MCP
Safety	Copilot PreToolUse Hook
Engineering & Governance

The project was developed using a structured Spec Kit workflow covering PRD, Constitution, Specification, Plan, Tasks, Implementation, Testing and Pull Request stages. The reference methodology emphasizes grounded and attributable answers, typed boundaries, quality gates, and keeping the API stateless.

GitHub MCP enables Copilot to interact with the repository and GitHub resources such as Issues and Pull Requests. A Copilot safety hook was also added to help prevent potentially destructive tool operations.

Safety Boundaries

RCA Buddy is strictly a decision-support system. It does not automatically deploy, rollback, delete, or modify production infrastructure. Recommended actions remain subject to human review and approval.

Secrets such as API keys are maintained outside source control.

Validation & Final Outcome

The application was successfully validated through local RCA execution, LLM integration, knowledge-base retrieval, backend testing, frontend build validation, GitHub Actions CI, GitHub MCP integration, and Copilot safety controls.

The final Pull Request #71 passed both backend and frontend checks and was successfully merged into the main branch.

Final Outcome

RCA Buddy demonstrates a practical implementation of RAG + LLM + vector search + modern API architecture + AI-assisted development + CI/CD governance to accelerate incident investigation while maintaining evidence-based responses and human control over remediation decisions.
