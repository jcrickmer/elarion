# NFR User Stories: Development Database Foundation

## Epic
**Development Database Platform (SQLite-first)**

Goal: Establish a reliable, repeatable, and safe database foundation for local development while keeping a clean path to future production database evolution.

## Stories

### DB-NFR1: Deterministic local DB bootstrap
**As** a developer, **I want** a one-command local database bootstrap, **so that** any contributor can start with a working database quickly.

**Acceptance Criteria**
- Running setup command creates database file and applies migrations.
- Command is idempotent.
- Setup instructions are documented in README or docs.

### DB-NFR2: Versioned schema migration discipline
**As** the team, **I want** schema changes managed through migrations only, **so that** schema evolution is reviewable and reproducible.

**Acceptance Criteria**
- New model changes require migration files.
- CI/local test command fails if unapplied model changes exist.
- Migration workflow is documented.

### DB-NFR3: Seed data for realistic dev workflows
**As** a developer/tester, **I want** optional seed data for worlds/campaigns/users, **so that** I can validate UI and behavior without manual setup.

**Acceptance Criteria**
- Seed command creates representative, non-production data.
- Re-running seed command is safe (no duplicate critical records).
- Seed data can be reset cleanly.

### DB-NFR4: Integrity and constraints baseline
**As** a product owner, **I want** key data constraints enforced at DB and model level, **so that** invalid relationships are prevented early.

**Acceptance Criteria**
- Core entity relationships have FK constraints and delete behavior defined.
- Uniqueness rules exist for critical identifiers/scopes.
- Constraint violations are covered by automated tests.

### DB-NFR5: Backup/restore for local safety
**As** a developer, **I want** simple backup and restore commands for SQLite, **so that** I can recover quickly from bad test data or schema mistakes.

**Acceptance Criteria**
- Backup command generates timestamped snapshots.
- Restore command can restore a selected snapshot.
- Commands are documented and tested manually.

### DB-NFR6: Test isolation and DB performance guardrails
**As** the team, **I want** reliable and fast test database behavior, **so that** CI/local feedback stays quick and trustworthy.

**Acceptance Criteria**
- Test suite uses isolated test DB, never shared dev DB.
- Test run time target is defined and tracked.
- Long-running or flaky DB tests are identified and categorized.

### DB-NFR7: Operational visibility in development
**As** a developer, **I want** basic DB observability in development, **so that** I can diagnose slow queries and data issues.

**Acceptance Criteria**
- Configurable query logging is available in dev mode.
- Slow-query threshold guidance is documented.
- Health-check endpoint validates DB connectivity.

### DB-NFR8: Security baseline for local data
**As** the team, **I want** basic local data protection practices, **so that** sensitive data is not accidentally exposed.

**Acceptance Criteria**
- Secrets/config are env-driven, not hardcoded.
- SQLite DB and backups are gitignored.
- Sample/dev credentials are non-sensitive and documented.
