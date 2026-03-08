from datetime import datetime, UTC
from pathlib import Path
import shutil

from django.conf import settings
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a timestamped SQLite backup snapshot for development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--label",
            default=None,
            help="Optional backup label. Defaults to UTC timestamp YYYYMMDD_HHMMSS.",
        )

    def handle(self, *args, **options):
        db_path = Path(settings.DATABASES["default"]["NAME"])
        if not db_path.exists():
            raise CommandError(f"Database file does not exist: {db_path}")

        backups_dir = db_path.parent / "backups"
        backups_dir.mkdir(parents=True, exist_ok=True)

        label = options["label"] or datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        backup_path = backups_dir / f"elarion_{label}.sqlite3"
        if backup_path.exists():
            raise CommandError(f"Backup target already exists: {backup_path}")

        shutil.copy2(db_path, backup_path)
        self.stdout.write(self.style.SUCCESS(f"Created backup: {backup_path}"))
