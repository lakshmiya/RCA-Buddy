import type { RcaReport as Report } from '../types';
import { ConfidenceBadge } from './ConfidenceBadge';
import { SimilarIncidents } from './SimilarIncidents';
import styles from '../styles/report.module.css';

type Props = { report: Report; onFileIssue: () => void };
export function RcaReport({ report, onFileIssue }: Props) {
  const low = report.confidence < 0.5;
  return <article className={`${styles.resultsColumn} ${styles.report}`} aria-live="polite" aria-labelledby="report-heading">
    <div className={styles.sectionHeading}>
      <div><p className={styles.eyebrow}>Step 02</p><h2 id="report-heading">Analysis results</h2></div>
      <span className={styles.completeLabel}>Complete</span>
    </div>
    {low && <div className={styles.uncertain} role="status"><strong>{report.uncertainty_message || "I'm not sure."}</strong><p>This result is low confidence and should be reviewed by an engineer.</p><button className={styles.secondary} type="button" onClick={onFileIssue}>File a GitHub issue <span aria-hidden="true">↗</span></button></div>}
    <div className={styles.resultCard}><div className={styles.cardLabel}><span className={styles.cardIcon}>◎</span><span>Probable root cause</span></div><p className={styles.rootCause}>{report.root_cause}</p><span className={styles.componentTag}>{report.component}</span></div>
    <div className={styles.resultGrid}>
      <div className={`${styles.resultCard} ${styles.confidenceCard}`}><div className={styles.cardLabel}><span className={styles.cardIcon}>◔</span><span>Confidence</span></div><ConfidenceBadge confidence={report.confidence} /></div>
      <div className={styles.resultCard}><div className={styles.cardLabel}><span className={styles.cardIcon}>✓</span><span>Recommended next steps</span></div><p>{report.suggested_fix}</p></div>
    </div>
    <SimilarIncidents incidents={report.similar_incidents} />
  </article>;
}
