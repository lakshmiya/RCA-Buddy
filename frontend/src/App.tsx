import { useEffect, useState } from 'react';
import { api } from './api/client';
import { useRca } from './hooks/useRca';
import { LogInput } from './components/LogInput';
import { RcaReport } from './components/RcaReport';
import { ErrorBanner } from './components/ErrorBanner';
import { FileIssueDialog } from './components/FileIssueDialog';
import { HealthStatus } from './components/HealthStatus';
import styles from './styles/report.module.css';
import './styles/tokens.css';

export default function App() {
	const rca = useRca();
	const [health, setHealth] = useState<Awaited<ReturnType<typeof api.health>> | null>(null);
	const [fileIssue, setFileIssue] = useState(false);

	useEffect(() => {
		api.health().then(setHealth).catch(() => setHealth(null));
	}, []);

	return (
		<div className={styles.shell}>
			<header className={styles.header}>
				<div className={styles.brandBlock}>
					<div className={styles.brandMark} aria-hidden="true">R</div>
					<div>
						<div className={styles.kicker}>Incident intelligence platform</div>
						<h1 className={styles.title}>RCA Buddy</h1>
						<p className={styles.subtitle}>AI-Powered CI/CD Incident Root Cause Analysis</p>
					</div>
				</div>
				<HealthStatus health={health} />
			</header>

			<main className={styles.main}>
				<section className={styles.intro} aria-labelledby="workspace-heading">
					<div>
						<p className={styles.eyebrow}>Analysis workspace</p>
						<h2 id="workspace-heading">Investigate a deployment failure</h2>
						<p>Turn noisy CI/CD output into a grounded explanation your team can act on.</p>
					</div>
					<div className={styles.safetyNote}>
						<span className={styles.safetyIcon} aria-hidden="true">i</span>
						<span>Decision support only — RCA Buddy does not automatically modify production systems.</span>
					</div>
				</section>

				<div className={styles.grid}>
					<section className={`${styles.panel} ${styles.inputPanel}`}>
						<div className={styles.sectionHeading}>
							<div>
								<p className={styles.eyebrow}>Step 01</p>
								<h2>Incident analysis</h2>
							</div>
							<span className={styles.stepLabel}>Required</span>
						</div>
						<LogInput loading={rca.loading} onSubmit={rca.submit} />
						{rca.error && <ErrorBanner error={rca.error} onRetry={rca.retry} />}
					</section>

					{rca.report ? (
						<RcaReport report={rca.report} onFileIssue={() => setFileIssue(true)} />
					) : (
						<section className={`${styles.panel} ${styles.emptyState}`} aria-label="Analysis results">
							<div className={styles.emptyIcon} aria-hidden="true">+</div>
							<p className={styles.eyebrow}>Step 02</p>
							<h2>Analysis results</h2>
							<p>Paste a failed CI/CD log to begin your root cause analysis.</p>
							<div className={styles.emptyDivider} />
							<span>Results will include confidence, evidence, and recommended next steps.</span>
						</section>
					)}
				</div>

				{fileIssue && rca.report && rca.request && <FileIssueDialog report={rca.report} request={rca.request} onClose={() => setFileIssue(false)} />}
			</main>
		</div>
	);
}
