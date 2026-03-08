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
    rules_system = models.OneToOneField(
        RulesSystem,
        on_delete=models.PROTECT,
        related_name="world",
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
