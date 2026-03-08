from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


SEED_USERS = [
    {
        "username": "gm_samantha",
        "email": "gm_samantha@example.com",
        "password": "ChangeMe123!",
        "is_staff": True,
        "is_superuser": False,
    },
    {
        "username": "player_rob",
        "email": "player_rob@example.com",
        "password": "ChangeMe123!",
        "is_staff": False,
        "is_superuser": False,
    },
    {
        "username": "player_tessa",
        "email": "player_tessa@example.com",
        "password": "ChangeMe123!",
        "is_staff": False,
        "is_superuser": False,
    },
]


class Command(BaseCommand):
    help = "Seed deterministic development users (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete seeded records before recreating them.",
        )

    def handle(self, *args, **options):
        user_model = get_user_model()
        usernames = [entry["username"] for entry in SEED_USERS]

        if options["reset"]:
            deleted_count, _ = user_model.objects.filter(username__in=usernames).delete()
            self.stdout.write(f"Reset requested: deleted {deleted_count} seeded users.")

        created = 0
        updated = 0
        for entry in SEED_USERS:
            user, was_created = user_model.objects.update_or_create(
                username=entry["username"],
                defaults={
                    "email": entry["email"],
                    "is_staff": entry["is_staff"],
                    "is_superuser": entry["is_superuser"],
                    "is_active": True,
                },
            )
            user.set_password(entry["password"])
            user.save(update_fields=["password"])
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed data ready. created={created}, updated={updated}, total_seed_users={len(SEED_USERS)}"
            )
        )
