PYTHON := .venv/bin/python
MANAGE := backend/manage.py

.PHONY: setup
setup:
	$(PYTHON) $(MANAGE) bootstrap_dev_db
