import type { ApiError } from '../api/client';
import styles from '../styles/report.module.css';
export function ErrorBanner({ error, onRetry }: { error: ApiError; onRetry: () => void }) { return <div className={styles.error} role="alert"><strong>We couldn't complete that analysis.</strong><p>{error.message}</p><details><summary>Technical details</summary><small>Code: {error.code} · Request ID: {error.requestId}</small></details><div className={styles.actions}><button className={styles.secondary} type="button" onClick={onRetry}>Retry</button></div></div>; }
