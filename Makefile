PYTHON := .venv/bin/python
MANAGE := backend/manage.py

.PHONY: setup check-migrations seed-dev-data seed-dev-data-reset seed-srd-baseline backup-db restore-db test test-report
setup:
	$(PYTHON) $(MANAGE) bootstrap_dev_db

check-migrations:
	$(PYTHON) $(MANAGE) makemigrations --check --dry-run

seed-dev-data:
	$(PYTHON) $(MANAGE) seed_dev_data

seed-dev-data-reset:
	$(PYTHON) $(MANAGE) seed_dev_data --reset

seed-srd-baseline:
	$(PYTHON) $(MANAGE) seed_srd_baseline

backup-db:
	$(PYTHON) $(MANAGE) backup_dev_db

restore-db:
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "Usage: make restore-db BACKUP_FILE=database/backups/<snapshot>.sqlite3"; \
		exit 1; \
	fi
	$(PYTHON) $(MANAGE) restore_dev_db --backup-file $(BACKUP_FILE)

test: check-migrations
	$(PYTHON) $(MANAGE) test apps.core -v 2

test-report:
	@if [ -f "reports/test-runtime-latest.json" ]; then \
		cat reports/test-runtime-latest.json; \
	else \
		echo "No runtime report found. Run 'make test' first."; \
		exit 1; \
	fi
