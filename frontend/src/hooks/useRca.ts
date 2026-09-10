import { useState } from 'react';
import { api, ApiError } from '../api/client';
import type { RcaReport, RcaRequest } from '../types';

export function useRca() {
  const [report, setReport] = useState<RcaReport | null>(null);
  const [error, setError] = useState<ApiError | null>(null);
  const [request, setRequest] = useState<RcaRequest | null>(null);
  const [loading, setLoading] = useState(false);

  async function submit(nextRequest: RcaRequest) {
    setRequest(nextRequest); setError(null); setLoading(true);
    try { setReport(await api.analyze(nextRequest)); } catch (caught) { setError(caught instanceof ApiError ? caught : new ApiError('NETWORK_ERROR', 'The service could not be reached.', 'unknown')); } finally { setLoading(false); }
  }
  async function retry() { if (request) await submit(request); }
  function reset() { setReport(null); setError(null); setRequest(null); }
  return { report, error, request, loading, submit, retry, reset };
}
