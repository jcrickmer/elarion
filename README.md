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
