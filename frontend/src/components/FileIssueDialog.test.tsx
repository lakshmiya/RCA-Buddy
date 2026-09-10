import { render, screen } from '@testing-library/react';
import { FileIssueDialog } from './FileIssueDialog';

test('labels issue dialog', () => { render(<FileIssueDialog report={{ root_cause: 'cause', component: 'c', confidence: .2, suggested_fix: 'fix', similar_incidents: [] }} request={{ log_text: 'log' }} onClose={() => undefined} />); expect(screen.getByRole('dialog')).toHaveAccessibleName('File a GitHub issue'); });
