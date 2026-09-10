import styles from '../styles/report.module.css';

export function ConfidenceBadge({ confidence }: { confidence: number }) {
  const low = confidence < 0.5;
  const percentage = Math.round(confidence * 100);
  return <div className={styles.confidence} aria-label={`${low ? 'Low' : 'High'} confidence: ${percentage} percent`}><div className={styles.confidenceValue}>{percentage}%</div><div className={styles.progressTrack} role="progressbar" aria-valuenow={percentage} aria-valuemin={0} aria-valuemax={100} aria-label="Confidence score"><span className={low ? styles.progressLow : styles.progressFill} style={{ width: `${percentage}%` }} /></div><span className={low ? styles.lowLabel : styles.highLabel}>{low ? 'Low confidence' : 'High confidence'}</span></div>;
}
