from django.db import models
from django.conf import settings


class RulesSystem(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128)
    edition = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["code"]


class World(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    rules_system = models.ForeignKey(
        RulesSystem,
        on_delete=models.PROTECT,
        related_name="worlds",
    )
    gm = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gm_worlds",
    )

    class Meta:
        ordering = ["name"]


class Campaign(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name="campaigns")
    name = models.CharField(max_length=128)
    slug = models.SlugField()

    class Meta:
        ordering = ["world_id", "name"]
        constraints = [
            models.UniqueConstraint(fields=["world", "name"], name="uniq_campaign_name_per_world"),
            models.UniqueConstraint(fields=["world", "slug"], name="uniq_campaign_slug_per_world"),
        ]


class Character(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name="characters")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="characters",
    )
    name = models.CharField(max_length=128)
    class_name = models.CharField(max_length=64)
    race_name = models.CharField(max_length=64)
    level = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["world_id", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["world", "owner", "name"], name="uniq_character_name_per_owner_world"
            ),
        ]


class CampaignCharacter(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="campaign_characters",
    )
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="campaign_links",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["campaign", "character"], name="uniq_campaign_character_link"
            )
        ]


class BaselineSpecies(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ["name"]


class BaselineClass(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=128)
    is_spellcaster = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]


class BaselineBackground(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ["name"]


class BaselineSpell(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=128)
    level = models.PositiveSmallIntegerField()
    school = models.CharField(max_length=64, blank=True)
    classes = models.ManyToManyField(BaselineClass, related_name="baseline_spells", blank=True)

    class Meta:
        ordering = ["level", "name"]


class BaselineItem(models.Model):
    CATEGORY_WEAPON = "weapon"
    CATEGORY_ARMOR = "armor"
    CATEGORY_GEAR = "gear"
    CATEGORY_TOOL = "tool"
    CATEGORY_CHOICES = [
        (CATEGORY_WEAPON, "Weapon"),
        (CATEGORY_ARMOR, "Armor"),
        (CATEGORY_GEAR, "Gear"),
        (CATEGORY_TOOL, "Tool"),
    ]

    code = models.SlugField(unique=True)
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES, default=CATEGORY_GEAR)
    suggested_for_classes = models.ManyToManyField(
        BaselineClass,
        related_name="suggested_baseline_items",
        blank=True,
    )

    class Meta:
        ordering = ["name"]


class BaselineClassSpellProgression(models.Model):
    character_class = models.ForeignKey(
        BaselineClass,
        on_delete=models.CASCADE,
        related_name="baseline_spell_progressions",
    )
    character_level = models.PositiveSmallIntegerField()
    spell_level = models.PositiveSmallIntegerField()
    slots = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["character_class_id", "character_level", "spell_level"]
        constraints = [
            models.UniqueConstraint(
                fields=["character_class", "character_level", "spell_level"],
                name="uniq_baseline_spell_progression_cell",
            )
        ]


class WorldSpecies(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name="world_species")
    code = models.SlugField()
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ["world_id", "name"]
        constraints = [
            models.UniqueConstraint(fields=["world", "code"], name="uniq_world_species_code")
        ]


class WorldClass(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name="world_classes")
    code = models.SlugField()
    name = models.CharField(max_length=128)
    is_spellcaster = models.BooleanField(default=False)

    class Meta:
        ordering = ["world_id", "name"]
        constraints = [
            models.UniqueConstraint(fields=["world", "code"], name="uniq_world_class_code")
        ]


class WorldBackground(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name="world_backgrounds")
    code = models.SlugField()
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ["world_id", "name"]
        constraints = [
            models.UniqueConstraint(fields=["world", "code"], name="uniq_world_background_code")
        ]


class WorldSpell(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name="world_spells")
    code = models.SlugField()
    name = models.CharField(max_length=128)
    level = models.PositiveSmallIntegerField()
    school = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["world_id", "level", "name"]
        constraints = [
            models.UniqueConstraint(fields=["world", "code"], name="uniq_world_spell_code")
        ]


class WorldSpellClassAvailability(models.Model):
    world_spell = models.ForeignKey(
        WorldSpell,
        on_delete=models.CASCADE,
        related_name="available_for_classes",
    )
    world_class = models.ForeignKey(
        WorldClass,
        on_delete=models.CASCADE,
        related_name="available_spells",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["world_spell", "world_class"],
                name="uniq_world_spell_class_availability",
            )
        ]


class WorldItem(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name="world_items")
    code = models.SlugField()
    name = models.CharField(max_length=128)
    category = models.CharField(
        max_length=16,
        choices=BaselineItem.CATEGORY_CHOICES,
        default=BaselineItem.CATEGORY_GEAR,
    )

    class Meta:
        ordering = ["world_id", "name"]
        constraints = [
            models.UniqueConstraint(fields=["world", "code"], name="uniq_world_item_code")
        ]


class WorldItemClassRecommendation(models.Model):
    world_item = models.ForeignKey(
        WorldItem,
        on_delete=models.CASCADE,
        related_name="recommended_for_classes",
    )
    world_class = models.ForeignKey(
        WorldClass,
        on_delete=models.CASCADE,
        related_name="recommended_items",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["world_item", "world_class"],
                name="uniq_world_item_class_recommendation",
            )
        ]


class WorldClassSpellProgression(models.Model):
    world = models.ForeignKey(
        World,
        on_delete=models.CASCADE,
        related_name="world_spell_progressions",
    )
    world_class = models.ForeignKey(
        WorldClass,
        on_delete=models.CASCADE,
        related_name="spell_progressions",
    )
    character_level = models.PositiveSmallIntegerField()
    spell_level = models.PositiveSmallIntegerField()
    slots = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["world_id", "world_class_id", "character_level", "spell_level"]
        constraints = [
            models.UniqueConstraint(
                fields=["world", "world_class", "character_level", "spell_level"],
                name="uniq_world_spell_progression_cell",
            )
        ]
