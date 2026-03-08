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
