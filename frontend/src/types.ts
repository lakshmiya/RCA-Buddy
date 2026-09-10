export type SimilarIncident = { id: string; title: string };
export type RcaRequest = { log_text?: string; source_url?: string | null };
export type RcaReport = { root_cause: string; component: string; confidence: number; suggested_fix: string; similar_incidents: SimilarIncident[]; is_grounded?: boolean; uncertainty_message?: string | null };
export type IssueRequest = { log_excerpt: string; rca_draft: string; confidence: number };
export type IssueResponse = { issue_url: string; issue_number: number };
export type HealthResponse = { status: string; model: string; vector_store: string; issues_configured: boolean };
export type ErrorDetail = { code: string; message: string; request_id: string; retry_after?: number };
