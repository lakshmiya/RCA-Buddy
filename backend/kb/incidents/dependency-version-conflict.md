# Dependency version conflict

- Failure signature: resolver conflict, incompatible package versions, or import behavior changed after an upgrade.
- Root cause: Two required packages cannot satisfy their version constraints together.
- Fix: Choose compatible versions, update the lock data, and verify the affected test path.
- Tags: dependency, version, resolver
