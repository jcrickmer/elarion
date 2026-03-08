# Test Quality Guardrails (DEV-27)

## Isolation
- Django tests run against an isolated test database (in-memory sqlite test DB in local runs), not `database/elarion.sqlite3`.
- Run tests with:
  `make test`

## Runtime target tracking
- Every test run writes a runtime report to:
  `reports/test-runtime-latest.json`
- Runtime target is configured by:
  - `TEST_RUNTIME_TARGET_SECONDS` (default `45`)
  - `TEST_SLOW_TEST_THRESHOLD_SECONDS` (default `0.5`)

## Slow tests identification
- Report includes:
  - total duration,
  - top 10 slowest tests,
  - list of tests slower than threshold.
- View report:
  `make test-report`

## Flaky tests identification
- Known flaky tests are tracked via `KNOWN_FLAKY_TESTS` in Django settings.
- Current state: no flaky tests registered.
- When a flaky test is discovered, add its full test ID to `KNOWN_FLAKY_TESTS` and create a dedicated fix ticket.
