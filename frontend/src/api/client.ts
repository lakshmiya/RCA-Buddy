import type { HealthResponse, IssueRequest, IssueResponse, RcaReport, RcaRequest } from '../types';

export class ApiError extends Error {
  constructor(public readonly code: string, message: string, public readonly requestId: string, public readonly retryAfter?: number) { super(message); }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, { headers: { 'Content-Type': 'application/json' }, ...init });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = data.error ?? { code: 'NETWORK_ERROR', message: 'The service could not complete the request.', request_id: 'unknown' };
    throw new ApiError(error.code, error.message, error.request_id, error.retry_after);
  }
  return data as T;
}

export const api = {
  analyze: (payload: RcaRequest) => request<RcaReport>('/api/rca', { method: 'POST', body: JSON.stringify(payload) }),
  createIssue: (payload: IssueRequest) => request<IssueResponse>('/api/issues', { method: 'POST', body: JSON.stringify(payload) }),
  health: () => request<HealthResponse>('/api/health'),
};
