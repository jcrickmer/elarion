from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Create and migrate the local development database (idempotent)."

    def handle(self, *args, **options):
        db_path = Path(settings.DATABASES["default"]["NAME"])
        db_path.parent.mkdir(parents=True, exist_ok=True)

        self.stdout.write(f"Using database file: {db_path}")
        call_command("migrate", interactive=False, verbosity=1)
        self.stdout.write(self.style.SUCCESS("Development database is ready."))
