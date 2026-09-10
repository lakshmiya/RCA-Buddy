# Docker build out of memory

- Failure signature: build process killed, exit code 137, or out-of-memory message during image build.
- Root cause: Build memory demand exceeds the available runner or image build limit.
- Fix: Reduce build context and parallel memory use, and allocate an appropriate build budget.
- Tags: docker, oom, build
