# Feature Specification: Grounded RCA Assistant

**Feature Branch**: `001-grounded-rca-assistant`

**Created**: 2026-09-10

**Status**: Draft

**Input**: User description: "Build RCA Buddy, an assistant that turns a failed CI/CD log into a grounded root-cause analysis."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Diagnose a pasted failure (Priority: P1)

As an engineer investigating a failed CI/CD run, I want to paste the failed log and receive an evidence-backed root-cause analysis so that I can understand what failed and what to do next without manually searching past incidents.

**Why this priority**: This is the core value of RCA Buddy and delivers a useful product even without the secondary hand-off and recovery workflows.

**Independent Test**: Submit a representative failed log containing a recognizable failure signature and verify that the returned report identifies the likely cause, affected component, confidence, suggested fix, and the similar incidents that informed it.

**Acceptance Scenarios**:

1. **Given** a user has a failed CI/CD log with a recognizable failure signature, **When** they submit the log, **Then** the assistant extracts the relevant failure details, finds matching past incidents, and returns a report with root cause, affected component, confidence from 0 to 1, suggested fix, and the matching incidents.
2. **Given** the submitted log has no matching past incidents, **When** analysis completes, **Then** the report shows an empty similar-incidents list and does not imply that an incident was used as evidence.
3. **Given** a user provides a source URL instead of or alongside log text, **When** they submit the request, **Then** the assistant uses the available request information to produce the same report shape or a clear actionable error.

### User Story 2 - Hand off uncertainty honestly (Priority: P2)

As an engineer whose failure cannot be diagnosed confidently, I want the assistant to say that it is unsure and let me file a GitHub issue with the investigation context so that a human can continue without losing the evidence.

**Why this priority**: Honest uncertainty prevents harmful guesses, while the hand-off preserves momentum when automated analysis is insufficient.

**Independent Test**: Submit an ambiguous log, verify that the report is explicitly low-confidence and offers "File a GitHub issue," then complete the hand-off and verify that the created issue URL is shown.

**Acceptance Scenarios**:

1. **Given** an analysis has insufficient supporting evidence, **When** the report is shown, **Then** it explicitly says the assistant is not sure, reports low confidence, and does not present a confident-sounding cause.
2. **Given** a low-confidence report, **When** the user selects "File a GitHub issue," **Then** a single interaction collects no additional required information and creates an issue containing the submitted log, the draft RCA, and the confidence score.
3. **Given** the issue is created successfully, **When** the hand-off completes, **Then** the user sees the created issue URL and issue number.
4. **Given** issue creation is unavailable or fails, **When** the user attempts the hand-off, **Then** the user sees an inline actionable error and the original report remains available.

### User Story 3 - Retry without retyping (Priority: P3)

As an engineer submitting a failure during a temporary service outage, I want to retry the original request without retyping the log so that a transient failure does not erase my work.

**Why this priority**: Recovery is essential for a trustworthy workflow, especially because logs are lengthy and costly to re-enter.

**Independent Test**: Submit a log while the service is unavailable, restart the service, select Retry, and verify that the original submission completes without additional input.

**Acceptance Scenarios**:

1. **Given** a submitted request fails, **When** the error is displayed, **Then** the interface shows an inline error with Retry and preserves the original log and source URL.
2. **Given** the service becomes available after a failed request, **When** the user selects Retry, **Then** the original request is resent and the resulting report is displayed without requiring the user to retype anything.
3. **Given** a request is rate-limited, **When** the error is displayed, **Then** the interface explains that the request can be retried and retains the original input.

### User Story 4 - Check service health (Priority: P4)

As an engineer using RCA Buddy, I want to see whether analysis and issue hand-off are ready so that I can understand service availability before or during an investigation.

**Why this priority**: Clear health status reduces wasted attempts and makes degraded dependencies visible without blocking the primary report workflow.

**Independent Test**: View the application with each dependency configured, unconfigured, and unavailable, and verify that the header distinguishes the model, vector store, and issue-creation statuses.

**Acceptance Scenarios**:

1. **Given** the service health information is available, **When** the user views the application header, **Then** the header shows the status of the model, vector store, and issue creation.
2. **Given** one dependency is unavailable or unconfigured, **When** health information is displayed, **Then** that dependency is visibly marked as unavailable or unconfigured while the other statuses remain understandable.
3. **Given** health information is unavailable, **When** the user views the header, **Then** the interface communicates an unknown or unavailable status rather than showing a false healthy state.

### User Story 5 - Use the report accessibly (Priority: P5)

As an engineer who uses a keyboard or screen reader, I want to inspect and act on an RCA report accessibly so that the incident workflow does not depend on a mouse, sight, or colour perception.

**Why this priority**: Accessibility is a requirement for the primary report workflow and ensures the product can be used by the full engineering team.

**Independent Test**: Navigate the report and its actions using only a keyboard and a screen reader, then verify labels, focus order, live announcements, and AA contrast.

**Acceptance Scenarios**:

1. **Given** a new RCA report is returned, **When** it appears, **Then** the report content is announced through a polite live region without interrupting unrelated activity.
2. **Given** the user navigates the report with a keyboard, **When** they move through controls and activate actions, **Then** every control has a meaningful label, receives visible focus, and can be operated without a mouse.
3. **Given** the report is displayed in supported states, **When** its text, controls, statuses, and confidence indicators are inspected, **Then** information is not conveyed by colour alone and colour contrast meets WCAG 2.1 AA.

### Edge Cases

- The submitted request contains neither usable log text nor a valid source URL; the user receives a clear validation message and no analysis is attempted.
- The log is very long; the assistant preserves the relevant failure signature and provides a useful error if the request cannot be processed, without silently claiming complete analysis.
- The log contains sensitive-looking values; the report and issue hand-off do not expose credentials or other secrets unnecessarily.
- The language model is unavailable or unconfigured; health status reflects the condition and analysis returns a clear recoverable error rather than a misleading report.
- The incident knowledge base is unavailable or empty; the assistant identifies the RCA as ungrounded or low-confidence when evidence is insufficient.
- Issue creation is unavailable; the user can still read the RCA and receives a clear explanation when hand-off cannot complete.
- A dependency fails after a report has been displayed; the existing report remains readable and is not replaced by an unrelated error.
- A user submits the same request again through Retry; the original request content is used exactly as preserved by the interface.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The assistant MUST accept a root-cause-analysis request containing log text, a source URL, or both, and MUST reject a request that contains neither usable log text nor a valid source URL with a clear validation message.
- **FR-002**: The assistant MUST identify and use the relevant failure signature, including the failing step, error or exception information, and relevant log lines, before producing an RCA.
- **FR-003**: The assistant MUST compare the failure signature with the available incident knowledge base and MUST identify the similar incidents that contributed to the report.
- **FR-004**: Every RCA report MUST include a probable root cause, affected component, confidence score between 0 and 1, suggested fix, and similar incidents used.
- **FR-005**: Every RCA that used the incident knowledge base MUST show which incidents were used; an RCA that used none MUST show an empty list and make that absence clear.
- **FR-006**: When evidence is insufficient or confidence is below the defined low-confidence threshold, the assistant MUST explicitly say it is not sure, report low confidence, and MUST NOT present a guessed cause as certain.
- **FR-007**: Every low-confidence RCA MUST offer a one-click "File a GitHub issue" action.
- **FR-008**: Filing an issue MUST include the submitted log or relevant log excerpt, the draft RCA, and the confidence score, and MUST return the created issue URL and issue number when successful.
- **FR-009**: If issue creation fails or is unavailable, the assistant MUST show an inline actionable error while keeping the RCA report available.
- **FR-010**: When a request fails, the interface MUST show an inline error with Retry and preserve the complete original request, including log text and source URL.
- **FR-011**: Selecting Retry MUST resend the preserved original request without requiring the user to retype or reselect it.
- **FR-012**: The interface MUST show the current status of the model, incident knowledge base, and issue-creation capability in the application header.
- **FR-013**: Health status MUST distinguish ready, unavailable, unconfigured, and unknown states where applicable and MUST NOT represent an unavailable dependency as healthy.
- **FR-014**: The RCA report view MUST have a polite live region for new report content, meaningful labels for all controls, visible keyboard focus, and keyboard-operable actions.
- **FR-015**: The RCA report view MUST meet WCAG 2.1 AA colour-contrast requirements and MUST NOT rely on colour alone to convey confidence, health, errors, or other meaning.
- **FR-016**: Client-facing failures MUST be understandable and actionable and MUST NOT expose raw internal stack traces or secret values.
- **FR-017**: The assistant MUST support the acceptance walkthrough in PRD §1.14, including a recognizable dependency failure, an ambiguous failure, issue hand-off, retry after service restart, and visible healthy service status.
- **FR-018**: The release MUST NOT include webhook auto-analysis, auto-remediation, Slack or Teams bot behavior, multi-repository dashboards, authentication, or non-GitHub CI provider support.

### Key Entities *(include if feature involves data)*

- **RCA Request**: The user-submitted log text and/or source URL used to request an analysis. It is request-scoped and is preserved for retry.
- **RCA Report**: The analysis returned to the user, containing root cause, affected component, confidence from 0 to 1, suggested fix, and similar incidents used.
- **Incident**: A knowledge-base write-up describing a title, failure signature, root cause, fix, and tags; it may be cited by an RCA report.
- **Issue**: A GitHub hand-off created from an uncertain investigation, identified to the user by its URL and number.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The complete acceptance walkthrough in PRD §1.14 passes end to end, including recognizable failure analysis, ambiguous failure handling, issue creation, retry after service restart, and healthy status.
- **SC-002**: 100% of RCA reports that use the incident knowledge base visibly identify every incident used to inform the report.
- **SC-003**: 100% of low-confidence RCA reports explicitly communicate uncertainty and offer "File a GitHub issue"; none presents a confident-sounding guess as an established cause.
- **SC-004**: A user can file an issue and see its created URL after one dialog interaction, without entering additional required investigation details.
- **SC-005**: After a failed request followed by service recovery, 100% of Retry attempts complete the original submission without requiring log re-entry.
- **SC-006**: In an accessibility review of the RCA report view, all controls are labelled and keyboard-operable, new reports are announced through a polite live region, and all applicable contrast checks meet WCAG 2.1 AA.
- **SC-007**: For each supported dependency condition, the header displays a status that matches the dependency's actual ready, unavailable, unconfigured, or unknown condition.
- **SC-008**: In a usability walkthrough, engineers can submit a valid failed log and locate the root cause, confidence, suggested fix, and evidence list without consulting external instructions.

## Assumptions

- Users are engineers who have a failed CI/CD log or a source URL and are authorized to submit that incident information.
- The initial release supports GitHub as the issue hand-off destination and the CI/CD source represented by the PRD; other CI providers are excluded.
- The confidence threshold for triggering uncertainty messaging is defined by the product release and is consistent across reports.
- Similar incidents are considered evidence only when they are actually used in producing the report.
- Log retention is request-scoped; the feature does not require persistent conversation history.
- The issue hand-off can use the submitted log or a relevant excerpt when the full log is too large, provided the resulting issue makes that limitation clear.
- Accessibility review covers the RCA report view and its actions, as required for this release.
- Authentication, multi-tenant accounts, automatic webhook analysis, automatic remediation, collaboration bots, and multi-repository dashboards remain out of scope.
