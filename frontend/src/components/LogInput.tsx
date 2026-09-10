import { useState } from 'react';
import type { RcaRequest } from '../types';
import styles from '../styles/report.module.css';

type Props = { loading: boolean; onSubmit: (request: RcaRequest) => void };
export function LogInput({ loading, onSubmit }: Props) {
  const [logText, setLogText] = useState('');
  const [sourceUrl, setSourceUrl] = useState('');
  function submit(event: React.FormEvent) {
    event.preventDefault();
    onSubmit({ log_text: logText, source_url: sourceUrl || null });
  }
  return <form onSubmit={submit} aria-label="Analyze a CI/CD failure">
    <div className={styles.fieldGroup}>
      <label className={styles.label} htmlFor="log-text">Failed CI/CD log</label>
      <p className={styles.fieldHint}>Include the failing step, exception, and stack trace when available.</p>
      <textarea id="log-text" className={styles.textarea} value={logText} onChange={(event) => setLogText(event.target.value)} placeholder={'Deploy production / build #1842\n\nERROR: Step \'Build image\' failed\nDockerfile:22: RUN npm run build\nerror: Cannot find module \'@acme/config\''} />
    </div>
    <div className={styles.fieldGroup}>
      <label className={styles.label} htmlFor="source-url">Run source URL <span className={styles.optional}>(optional)</span></label>
      <input id="source-url" className={styles.input} value={sourceUrl} onChange={(event) => setSourceUrl(event.target.value)} placeholder="https://github.com/org/repo/actions/runs/..." type="url" />
    </div>
    <div className={styles.actions}>
      <button className={styles.primary} type="submit" disabled={loading}>
        {loading ? <><span className={styles.spinner} aria-hidden="true" />Analyzing incident...</> : <>Analyze incident <span aria-hidden="true">→</span></>}
      </button>
    </div>
  </form>;
}
