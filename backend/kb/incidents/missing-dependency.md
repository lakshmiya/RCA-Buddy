# Missing dependency

- Failure signature: ImportError or ModuleNotFoundError during tests or application startup.
- Root cause: A package used by the failing component is absent from the declared dependencies.
- Fix: Add the missing package to the dependency manifest and rebuild the environment.
- Tags: importerror, dependency, pytest
