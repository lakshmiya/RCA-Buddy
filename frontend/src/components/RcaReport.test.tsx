import { render, screen } from '@testing-library/react';
import { RcaReport } from './RcaReport';

test('renders report content and polite live region', () => { render(<RcaReport report={{ root_cause: 'Missing package', component: 'tests', confidence: .88, suggested_fix: 'Add dependency', similar_incidents: [{ id: 'missing-dependency', title: 'Missing dependency' }] }} onFileIssue={() => undefined} />); expect(screen.getByRole('article')).toHaveAttribute('aria-live', 'polite'); expect(screen.getByText('Missing package')).toBeInTheDocument(); expect(screen.getByText('Missing dependency')).toBeInTheDocument(); });
