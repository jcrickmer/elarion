from django.core.management import BaseCommand

from apps.core.world_import import (
    GROUP_BACKGROUNDS,
    GROUP_CLASSES,
    GROUP_ITEMS,
    GROUP_SPECIES,
    GROUP_SPELLS,
    VALID_GROUPS,
    WorldImportRequest,
    create_world_from_srd_baseline,
)


class Command(BaseCommand):
    help = "Create a world by selecting SRD concept groups to import."

    def add_arguments(self, parser):
        parser.add_argument("--world-name", required=True)
        parser.add_argument("--world-slug", required=True)
        parser.add_argument("--gm-username", required=True)
        parser.add_argument(
            "--include",
            default=",".join(
                [GROUP_SPECIES, GROUP_CLASSES, GROUP_SPELLS, GROUP_ITEMS, GROUP_BACKGROUNDS]
            ),
            help="Comma-separated include groups: species,classes,spells,items,backgrounds",
        )

    def handle(self, *args, **options):
        include_groups = {
            part.strip().lower() for part in options["include"].split(",") if part.strip()
        }
        unknown = include_groups - VALID_GROUPS
        if unknown:
            raise ValueError(f"Unknown include groups: {sorted(unknown)}")

        request = WorldImportRequest(
            world_name=options["world_name"],
            world_slug=options["world_slug"],
            gm_username=options["gm_username"],
            include_groups=include_groups,
        )
        world = create_world_from_srd_baseline(request)
        self.stdout.write(
            self.style.SUCCESS(
                f"Created world '{world.name}' ({world.slug}) with include groups: {sorted(include_groups)}"
            )
        )
