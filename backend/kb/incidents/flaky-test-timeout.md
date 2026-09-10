# Flaky test timeout

- Failure signature: test timeout or intermittent job timeout with no deterministic assertion failure.
- Root cause: A timing-sensitive test or shared resource occasionally exceeds the job budget.
- Fix: Isolate the resource, remove uncontrolled waits, and tune the test timeout based on evidence.
- Tags: timeout, flaky, test
