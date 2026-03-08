PYTHON := .venv/bin/python
MANAGE := backend/manage.py

.PHONY: setup check-migrations test
setup:
	$(PYTHON) $(MANAGE) bootstrap_dev_db

check-migrations:
	$(PYTHON) $(MANAGE) makemigrations --check --dry-run

test: check-migrations
	$(PYTHON) $(MANAGE) test apps.core -v 2
