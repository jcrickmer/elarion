# DB Observability Baseline (DEV-28)

## DB health endpoint
- Endpoint: `GET /health/db/`
- Success response: `200 {"status":"ok","db":"reachable"}`
- Failure response: `503 {"status":"error","db":"unreachable",...}`

Use this endpoint for quick development checks and container health probes.

## Configurable SQL query logging
Enable SQL query logging in development with:
- `DB_QUERY_LOGGING_ENABLED=1`
- Optional: `DB_QUERY_LOGGING_LEVEL=DEBUG`

Default behavior keeps query logs quiet (`WARNING`) unless enabled.

## Slow-query guidance
- Start threshold: `DB_SLOW_QUERY_THRESHOLD_MS=200`
- If repeated queries exceed threshold in local runs, investigate:
  - missing indexes,
  - N+1 query patterns,
  - unnecessary repeated reads,
  - unbounded list queries.

Recommended local workflow:
1. Enable query logging.
2. Reproduce slow request path.
3. Capture SQL statements and timings.
4. Add optimization/fix ticket with measured before/after.
