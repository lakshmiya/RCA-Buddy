import type { SimilarIncident } from '../types';
import styles from '../styles/report.module.css';
export function SimilarIncidents({ incidents }: { incidents: SimilarIncident[] }) {
  return <section className={styles.sourcesCard} aria-labelledby="evidence-heading"><div className={styles.cardLabel}><span className={styles.cardIcon}>⌁</span><span id="evidence-heading">Knowledge base sources</span></div>{incidents.length ? <ul className={styles.incidents}>{incidents.map((incident) => <li key={incident.id}><span className={styles.sourceDot} aria-hidden="true" /><span><strong>{incident.title}</strong><small>Incident knowledge base</small></span></li>)}</ul> : <p className={styles.muted}>No similar incidents were used.</p>}</section>;
}
