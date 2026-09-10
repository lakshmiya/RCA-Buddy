import { render, screen } from '@testing-library/react';
import { ErrorBanner } from './ErrorBanner';
import { ApiError } from '../api/client';

test('offers retry', () => { render(<ErrorBanner error={new ApiError('X', 'Try again', 'r')} onRetry={() => undefined} />); expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument(); });
