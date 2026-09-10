import { render, screen } from '@testing-library/react';
import { LogInput } from './LogInput';

test('log input controls are labelled', () => { render(<LogInput loading={false} onSubmit={() => undefined} />); expect(screen.getByLabelText('Failed CI/CD log')).toBeInTheDocument(); expect(screen.getByLabelText('Run source URL (optional)')).toBeInTheDocument(); });
