from django.core.management import BaseCommand

from apps.core.models import (
    BaselineBackground,
    BaselineClass,
    BaselineClassSpellProgression,
    BaselineItem,
    BaselineSpecies,
)


class Command(BaseCommand):
    help = "Seed a focused SRD baseline dataset for world initialization (idempotent)."

    def handle(self, *args, **options):
        species = [
            ("human", "Human"),
            ("elf", "Elf"),
            ("dwarf", "Dwarf"),
        ]
        classes = [
            ("fighter", "Fighter", False),
            ("cleric", "Cleric", True),
            ("magic-user", "Magic User", True),
            ("thief", "Thief", False),
        ]
        backgrounds = [
            ("soldier", "Soldier"),
            ("acolyte", "Acolyte"),
            ("criminal", "Criminal"),
        ]

        for code, name in species:
            BaselineSpecies.objects.update_or_create(code=code, defaults={"name": name})

        class_map = {}
        for code, name, is_spellcaster in classes:
            cls, _ = BaselineClass.objects.update_or_create(
                code=code,
                defaults={"name": name, "is_spellcaster": is_spellcaster},
            )
            class_map[code] = cls

        for code, name in backgrounds:
            BaselineBackground.objects.update_or_create(code=code, defaults={"name": name})

        # Spells: enough across levels for progression demonstration.
        spell_rows = [
            ("cure-wounds", "Cure Wounds", 1, "Evocation", ["cleric"]),
            ("bless", "Bless", 1, "Enchantment", ["cleric"]),
            ("spiritual-weapon", "Spiritual Weapon", 2, "Evocation", ["cleric"]),
            ("revivify", "Revivify", 3, "Necromancy", ["cleric"]),
            ("magic-missile", "Magic Missile", 1, "Evocation", ["magic-user"]),
            ("shield", "Shield", 1, "Abjuration", ["magic-user"]),
            ("misty-step", "Misty Step", 2, "Conjuration", ["magic-user"]),
            ("fireball", "Fireball", 3, "Evocation", ["magic-user"]),
            ("invisibility", "Invisibility", 2, "Illusion", ["magic-user"]),
        ]

        from apps.core.models import BaselineSpell

        for code, name, level, school, class_codes in spell_rows:
            spell, _ = BaselineSpell.objects.update_or_create(
                code=code,
                defaults={"name": name, "level": level, "school": school},
            )
            spell.classes.set([class_map[c] for c in class_codes])

        item_rows = [
            ("longsword", "Longsword", BaselineItem.CATEGORY_WEAPON, ["fighter"]),
            ("shield", "Shield", BaselineItem.CATEGORY_ARMOR, ["fighter", "cleric"]),
            ("mace", "Mace", BaselineItem.CATEGORY_WEAPON, ["cleric"]),
            ("holy-symbol", "Holy Symbol", BaselineItem.CATEGORY_GEAR, ["cleric"]),
            ("spellbook", "Spellbook", BaselineItem.CATEGORY_GEAR, ["magic-user"]),
            ("dagger", "Dagger", BaselineItem.CATEGORY_WEAPON, ["magic-user", "thief"]),
            ("shortbow", "Shortbow", BaselineItem.CATEGORY_WEAPON, ["thief"]),
            ("thieves-tools", "Thieves' Tools", BaselineItem.CATEGORY_TOOL, ["thief"]),
            ("leather-armor", "Leather Armor", BaselineItem.CATEGORY_ARMOR, ["thief"]),
            ("chain-mail", "Chain Mail", BaselineItem.CATEGORY_ARMOR, ["fighter", "cleric"]),
            ("rope-hempen", "Rope (Hempen)", BaselineItem.CATEGORY_GEAR, ["fighter", "thief"]),
            ("torch", "Torch", BaselineItem.CATEGORY_GEAR, ["fighter", "cleric", "magic-user", "thief"]),
            ("rations", "Rations", BaselineItem.CATEGORY_GEAR, ["fighter", "cleric", "magic-user", "thief"]),
        ]

        for code, name, category, class_codes in item_rows:
            item, _ = BaselineItem.objects.update_or_create(
                code=code,
                defaults={"name": name, "category": category},
            )
            item.suggested_for_classes.set([class_map[c] for c in class_codes])

        # Basic progression tables (levels 1-5).
        progression_cells = [
            # Cleric
            ("cleric", 1, 1, 2),
            ("cleric", 2, 1, 3),
            ("cleric", 3, 1, 4),
            ("cleric", 3, 2, 2),
            ("cleric", 4, 1, 4),
            ("cleric", 4, 2, 3),
            ("cleric", 5, 1, 4),
            ("cleric", 5, 2, 3),
            ("cleric", 5, 3, 2),
            # Magic User
            ("magic-user", 1, 1, 2),
            ("magic-user", 2, 1, 3),
            ("magic-user", 3, 1, 4),
            ("magic-user", 3, 2, 2),
            ("magic-user", 4, 1, 4),
            ("magic-user", 4, 2, 3),
            ("magic-user", 5, 1, 4),
            ("magic-user", 5, 2, 3),
            ("magic-user", 5, 3, 2),
        ]

        for class_code, character_level, spell_level, slots in progression_cells:
            BaselineClassSpellProgression.objects.update_or_create(
                character_class=class_map[class_code],
                character_level=character_level,
                spell_level=spell_level,
                defaults={"slots": slots},
            )

        self.stdout.write(self.style.SUCCESS("Seeded focused SRD baseline dataset."))
