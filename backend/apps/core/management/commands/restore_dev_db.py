from pathlib import Path
import shutil

from django.conf import settings
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Restore the development SQLite database from an explicit backup snapshot."

    def add_arguments(self, parser):
        parser.add_argument(
            "--backup-file",
            required=True,
            help="Path to backup .sqlite3 file to restore from.",
        )

    def handle(self, *args, **options):
        backup_path = Path(options["backup_file"]).expanduser()
        if not backup_path.exists():
            raise CommandError(f"Backup file does not exist: {backup_path}")

        db_path = Path(settings.DATABASES["default"]["NAME"])
        db_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(backup_path, db_path)
        self.stdout.write(self.style.SUCCESS(f"Restored database from: {backup_path}"))
