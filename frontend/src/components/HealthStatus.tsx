import type { HealthResponse } from '../types';
import styles from '../styles/report.module.css';
export function HealthStatus({ health }: { health: HealthResponse | null }) {
	if (!health) return <div className={styles.systemStatus}><span className={`${styles.statusDot} ${styles.statusUnknown}`} /> <span>System status <strong>Unknown</strong></span></div>;
	return <div className={styles.systemStatus} aria-label="Service health"><span className={`${styles.statusDot} ${health.status === 'ok' ? styles.statusReady : styles.statusUnknown}`} /><div><span className={styles.statusTitle}>System status</span><strong>Operational</strong></div><div className={styles.statusDetails}><span>Model: {health.model}</span><span>Vector store: {health.vector_store}</span><span>Issues: {health.issues_configured ? 'ready' : 'unconfigured'}</span></div></div>;
}
