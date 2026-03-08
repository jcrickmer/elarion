from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db import transaction

from .models import (
    BaselineBackground,
    BaselineClass,
    BaselineClassSpellProgression,
    BaselineItem,
    BaselineSpecies,
    BaselineSpell,
    RulesSystem,
    World,
    WorldBackground,
    WorldClass,
    WorldClassSpellProgression,
    WorldItem,
    WorldItemClassRecommendation,
    WorldSpecies,
    WorldSpell,
    WorldSpellClassAvailability,
)

GROUP_SPECIES = "species"
GROUP_CLASSES = "classes"
GROUP_SPELLS = "spells"
GROUP_ITEMS = "items"
GROUP_BACKGROUNDS = "backgrounds"
VALID_GROUPS = {
    GROUP_SPECIES,
    GROUP_CLASSES,
    GROUP_SPELLS,
    GROUP_ITEMS,
    GROUP_BACKGROUNDS,
}


@dataclass(frozen=True)
class WorldImportRequest:
    world_name: str
    world_slug: str
    gm_username: str
    include_groups: set[str]


@transaction.atomic
def create_world_from_srd_baseline(request: WorldImportRequest) -> World:
    unknown = request.include_groups - VALID_GROUPS
    if unknown:
        raise ValueError(f"Unknown include groups: {sorted(unknown)}")
    if GROUP_SPELLS in request.include_groups and GROUP_CLASSES not in request.include_groups:
        raise ValueError("Including spells requires including classes for progression mapping.")

    user = get_user_model().objects.get(username=request.gm_username)
    rules_system, _ = RulesSystem.objects.get_or_create(
        code="dnd5e-2024",
        defaults={"name": "D&D 5e", "edition": "2024"},
    )

    world = World.objects.create(
        name=request.world_name,
        slug=request.world_slug,
        rules_system=rules_system,
        gm=user,
    )

    world_classes_by_code = {}

    if GROUP_SPECIES in request.include_groups:
        WorldSpecies.objects.bulk_create(
            [WorldSpecies(world=world, code=entry.code, name=entry.name) for entry in BaselineSpecies.objects.all()]
        )

    if GROUP_CLASSES in request.include_groups:
        world_classes = [
            WorldClass(
                world=world,
                code=entry.code,
                name=entry.name,
                is_spellcaster=entry.is_spellcaster,
            )
            for entry in BaselineClass.objects.all()
        ]
        WorldClass.objects.bulk_create(world_classes)
        world_classes_by_code = {entry.code: entry for entry in WorldClass.objects.filter(world=world)}

    if GROUP_BACKGROUNDS in request.include_groups:
        WorldBackground.objects.bulk_create(
            [
                WorldBackground(world=world, code=entry.code, name=entry.name)
                for entry in BaselineBackground.objects.all()
            ]
        )

    if GROUP_SPELLS in request.include_groups:
        baseline_spells = list(BaselineSpell.objects.prefetch_related("classes"))
        WorldSpell.objects.bulk_create(
            [
                WorldSpell(
                    world=world,
                    code=spell.code,
                    name=spell.name,
                    level=spell.level,
                    school=spell.school,
                )
                for spell in baseline_spells
            ]
        )
        world_spells_by_code = {entry.code: entry for entry in WorldSpell.objects.filter(world=world)}

        availability_rows = []
        for spell in baseline_spells:
            for baseline_class in spell.classes.all():
                world_class = world_classes_by_code.get(baseline_class.code)
                if world_class:
                    availability_rows.append(
                        WorldSpellClassAvailability(
                            world_spell=world_spells_by_code[spell.code],
                            world_class=world_class,
                        )
                    )
        WorldSpellClassAvailability.objects.bulk_create(availability_rows)

        progression_rows = []
        for cell in BaselineClassSpellProgression.objects.select_related("character_class"):
            world_class = world_classes_by_code.get(cell.character_class.code)
            if world_class:
                progression_rows.append(
                    WorldClassSpellProgression(
                        world=world,
                        world_class=world_class,
                        character_level=cell.character_level,
                        spell_level=cell.spell_level,
                        slots=cell.slots,
                    )
                )
        WorldClassSpellProgression.objects.bulk_create(progression_rows)

    if GROUP_ITEMS in request.include_groups:
        baseline_items = list(BaselineItem.objects.prefetch_related("suggested_for_classes"))
        WorldItem.objects.bulk_create(
            [
                WorldItem(
                    world=world,
                    code=item.code,
                    name=item.name,
                    category=item.category,
                )
                for item in baseline_items
            ]
        )
        world_items_by_code = {entry.code: entry for entry in WorldItem.objects.filter(world=world)}
        rec_rows = []
        for item in baseline_items:
            for baseline_class in item.suggested_for_classes.all():
                world_class = world_classes_by_code.get(baseline_class.code)
                if world_class:
                    rec_rows.append(
                        WorldItemClassRecommendation(
                            world_item=world_items_by_code[item.code],
                            world_class=world_class,
                        )
                    )
        WorldItemClassRecommendation.objects.bulk_create(rec_rows)

    return world
