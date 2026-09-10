import { render, screen } from '@testing-library/react';
import { HealthStatus } from './HealthStatus';

test('shows dependency statuses', () => { render(<HealthStatus health={{ status: 'ok', model: 'ready', vector_store: 'ok', issues_configured: false }} />); expect(screen.getByText('Model: ready')).toBeInTheDocument(); expect(screen.getByText('Issues: unconfigured')).toBeInTheDocument(); });
