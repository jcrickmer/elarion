PYTHON := .venv/bin/python
MANAGE := backend/manage.py

.PHONY: setup check-migrations seed-dev-data seed-dev-data-reset test
setup:
	$(PYTHON) $(MANAGE) bootstrap_dev_db

check-migrations:
	$(PYTHON) $(MANAGE) makemigrations --check --dry-run

seed-dev-data:
	$(PYTHON) $(MANAGE) seed_dev_data

seed-dev-data-reset:
	$(PYTHON) $(MANAGE) seed_dev_data --reset

test: check-migrations
	$(PYTHON) $(MANAGE) test apps.core -v 2
