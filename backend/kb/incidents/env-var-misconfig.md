# Environment variable misconfiguration

- Failure signature: missing configuration, authentication failure, or service startup error caused by an absent variable.
- Root cause: Required environment variable is missing, misspelled, or not available in the execution environment.
- Fix: Validate required configuration at startup and correct the environment entry without logging its value.
- Tags: environment, configuration, secret
