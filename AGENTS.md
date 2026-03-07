# Repository Guidelines

## Project Structure & Module Organization
This project is a web-delivered app with an HTML/JavaScript frontend and a Python 3.12+ backend using SQLite3.

- `backend/`: Python server code (`app.py`, routes, services, data access).
- `frontend/`: browser assets (`index.html`, `css/`, `js/`).
- `database/`: SQLite files, schema, and migrations (`schema.sql`, `migrations/`).
- `tests/`: backend and frontend tests, mirroring runtime modules.
- `scripts/`: local automation (db init, lint, test, run helpers).

Example:
`backend/auth/service.py` pairs with `tests/backend/auth/test_service.py`.

## Build, Test, and Development Commands
Standardize these command entry points and keep them stable:

- `make setup`: create `.venv`, install Python dependencies, and initialize SQLite schema.
- `make test`: run the full test suite.
- `make lint`: run Python and JavaScript linters/formatters.
- `make run`: start the Python web server and serve frontend assets.
- `python -m pytest`: direct backend test execution.
- `python -m sqlite3 database/app.db ".tables"`: quick SQLite verification.

## Coding Style & Naming Conventions
- Python: 4-space indentation, type hints for public functions, `snake_case` modules, `PascalCase` classes.
- JavaScript/HTML/CSS: follow consistent formatting with 2-space indentation in frontend files.
- Use descriptive names (`user_repository.py`, `session-store.js`).
- Keep route handlers thin; move business logic to services.
- Run `ruff format`/`ruff check` for Python and `eslint`/`prettier` for frontend code.

## Testing Guidelines
- Frameworks: `pytest` for backend; use a JS test runner (for example, `vitest` or `jest`) for frontend logic.
- Mirror source paths under `tests/`.
- Naming: Python tests as `test_<module>.py`; frontend tests as `<module>.test.js`.
- Include API, data-layer, and regression tests for any bug fix.
- Prefer isolated SQLite test databases/fixtures, not the main local DB file.

## Commit & Pull Request Guidelines
Use Conventional Commits:
- `feat: add user session cache`
- `fix: handle null token in auth middleware`

PRs should include:
- clear summary and rationale,
- linked issue/ticket when available,
- test evidence (`make test`, lint output, or CI link),
- screenshots for frontend changes and request/response examples for API changes.

Keep PRs focused and small enough for fast review.
