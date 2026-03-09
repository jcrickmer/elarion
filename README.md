# elarion
Tabletop RPG collaborator for in-person play groups

## Development Setup
1. Create and activate virtual environment:
   `python3.12 -m venv .venv && source .venv/bin/activate`
2. Install dependencies:
   `pip install -r requirements.txt`
3. Bootstrap local database (idempotent):
   `make setup`

The setup command creates the local SQLite database path and applies all Django migrations.

## Migration Workflow Discipline
- Create migrations after model changes:
  `./.venv/bin/python backend/manage.py makemigrations`
- Apply migrations:
  `./.venv/bin/python backend/manage.py migrate`
- Verify no uncommitted model changes remain:
  `make check-migrations`

`make check-migrations` runs `makemigrations --check --dry-run` and exits non-zero when model changes are missing migration files.

## Test Workflow
- Run test suite with migration guard:
  `make test`

`make test` runs `check-migrations` first, then executes Django tests.

## Tailwind UI Pipeline (DEV-59)
- Install Node dependencies:
  `make ui-install`
- Build production CSS from Tailwind source:
  `make ui-build`
- Run Tailwind in watch mode during template work:
  `make ui-watch`

Tailwind source and output paths:
- Source entrypoint: `frontend/static/src/tailwind.css`
- Compiled output: `frontend/static/css/main.css`
- Config: `tailwind.config.js`

The source includes base theme tokens and reusable UI primitives:
- `.ui-shell`
- `.ui-card`
- `.ui-page` / `.ui-nav` / `.ui-nav-link`
- `.ui-title` / `.ui-subtitle` / `.ui-section-title` / `.ui-text-muted`
- `.ui-btn-primary`
- `.ui-btn-secondary`
- `.ui-badge` / `.ui-badge-success`
- `.ui-form` / `.ui-form-row` / `.ui-form-label` / `.ui-form-help`
- `.ui-input`
- `.ui-alert` / `.ui-alert-error` / `.ui-alert-success`

## Authentication Security Defaults
- Password hashing uses Django's built-in secure password hashing.
- Session/CSRF cookies are HTTP-only and `SameSite=Lax` by default.
- Login is rate-limited per username + IP (default: 5 failed attempts per 15 minutes).
- Auth events are logged (`login_failed`, `login_success`, `logout`) via `apps.core.auth` logger.

You can tune throttling with environment variables:
- `LOGIN_RATE_LIMIT_ATTEMPTS`
- `LOGIN_RATE_LIMIT_WINDOW_SECONDS`

## Development Seed Data
- Seed deterministic dev users:
  `make seed-dev-data`
- Reset and reseed:
  `make seed-dev-data-reset`

The seed command is idempotent and currently creates representative GM/player accounts for local testing:
- `gm_samantha`
- `player_rob`
- `player_tessa`

## Focused SRD Baseline and World Import (DEV-36)
- Seed focused SRD baseline dataset:
  `make seed-srd-baseline`
- Create a world from selected SRD groups:
  `./.venv/bin/python backend/manage.py create_world_from_srd --world-name \"Sable Reach\" --world-slug sable-reach --gm-username <username> --include species,classes,spells,items`

Supported include groups:
- `species`
- `classes`
- `spells` (requires `classes`)
- `items`
- `backgrounds`

## SQLite Backup and Restore (DEV-26)
- Create timestamped backup snapshot:
  `make backup-db`
- Restore from explicit snapshot:
  `make restore-db BACKUP_FILE=database/backups/<snapshot>.sqlite3`

Notes:
- Backups are written under `database/backups/` as `elarion_<timestamp>.sqlite3`.
- Restore requires an explicit file path and overwrites the current development DB.

## DB Observability (DEV-28)
- DB health endpoint:
  `GET /health/db/`
- Enable SQL query logging in dev:
  - `DB_QUERY_LOGGING_ENABLED=1`
  - optional `DB_QUERY_LOGGING_LEVEL=DEBUG`
- Slow query guidance threshold:
  - `DB_SLOW_QUERY_THRESHOLD_MS` (default `200`)

See details:
- `docs/db_observability.md`
