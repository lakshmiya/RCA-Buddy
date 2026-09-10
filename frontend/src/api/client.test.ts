import { vi } from 'vitest';
import { api, ApiError } from './client';

test('maps structured API errors', async () => { vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, json: async () => ({ error: { code: 'RATE_LIMITED', message: 'Retry', request_id: 'r1', retry_after: 3 } }) })); await expect(api.analyze({ log_text: 'x' })).rejects.toEqual(expect.any(ApiError)); await expect(api.analyze({ log_text: 'x' })).rejects.toMatchObject({ code: 'RATE_LIMITED', requestId: 'r1', retryAfter: 3 }); });
