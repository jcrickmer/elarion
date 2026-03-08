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
