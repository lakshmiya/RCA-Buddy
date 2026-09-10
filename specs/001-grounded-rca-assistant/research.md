# Research Notes

- Google AI Studio calls use a configured model name and structured response parsing; provider configuration and failures are isolated in `GeminiClient`.
- ChromaDB uses a persistent local client and a deterministic embedding function for the incident corpus. Retrieval returns top-k matches only above a configured threshold and safely returns an empty list when the corpus is unavailable.
- GitHub issue creation uses an authenticated REST request; provider rate limits become a typed retryable error and credentials never enter logs or responses.
- Log parsing is deterministic: identify CI step headings, exception/error lines, and contiguous traceback lines before passing a compact signature to retrieval and the model.

These choices are intentionally isolated behind Protocols so tests can use controlled doubles.
