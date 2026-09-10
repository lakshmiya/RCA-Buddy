import { render, screen } from '@testing-library/react';
import { RcaReport } from './RcaReport';

test('report is politely announced and actionable when uncertain', () => { render(<RcaReport report={{ root_cause: 'Unknown', component: 'tests', confidence: .2, suggested_fix: 'Investigate', similar_incidents: [], uncertainty_message: "I'm not sure." }} onFileIssue={() => undefined} />); expect(screen.getByRole('article')).toHaveAttribute('aria-live', 'polite'); expect(screen.getByRole('button', { name: 'File a GitHub issue' })).toBeEnabled(); });
