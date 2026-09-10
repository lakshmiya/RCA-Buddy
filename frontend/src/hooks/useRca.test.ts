import { renderHook, act } from '@testing-library/react';
import { useRca } from './useRca';
import { api } from '../api/client';
import type { RcaReport } from '../types';
import { vi } from 'vitest';

const report: RcaReport = { root_cause: 'cause', component: 'component', confidence: .8, suggested_fix: 'fix', similar_incidents: [] };
test('preserves request for retry', async () => { vi.spyOn(api, 'analyze').mockResolvedValue(report); const hook = renderHook(() => useRca()); await act(() => hook.result.current.submit({ log_text: 'log' })); expect(hook.result.current.request).toEqual({ log_text: 'log' }); await act(() => hook.result.current.retry()); expect(api.analyze).toHaveBeenCalledTimes(2); });
