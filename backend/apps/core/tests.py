from django.urls import reverse
from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, override_settings
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from io import StringIO
from django.core.management import call_command
from django.core.cache import cache
from apps.core.management.commands.seed_dev_data import SEED_USERS
from apps.core.models import (
    BaselineClass,
    BaselineItem,
    BaselineSpecies,
    Campaign,
    CampaignCharacter,
    Character,
    RulesSystem,
    World,
    WorldClass,
    WorldItem,
    WorldSpecies,
    WorldSpell,
    WorldClassSpellProgression,
)


class TestHomePage(TestCase):
    def test_home_page_shows_value_prop_benefits_and_ctas(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Elarion keeps players and GMs synchronized while staying focused on tabletop storytelling.",
        )
        self.assertContains(response, "For Players")
        self.assertContains(response, "For Game Masters")
        self.assertContains(response, "Log in")
        self.assertContains(response, "Create account")

    def test_home_page_links_to_login_and_signup_routes(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, f'href="{reverse("login")}"')
        self.assertContains(response, f'href="{reverse("signup")}"')

    def test_home_page_includes_scope_clarification_and_docs_link(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Elarion Focus")
        self.assertContains(response, "It is not a full virtual tabletop")
        self.assertContains(response, "Read the product overview")
        self.assertContains(response, f'href="{reverse("product_overview")}"')

    def test_product_overview_page_is_available(self):
        response = self.client.get(reverse("product_overview"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product Overview")

    def test_authenticated_user_is_redirected_from_home_to_dashboard(self):
        user = get_user_model().objects.create_user(
            username="rob",
            email="rob@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("home"))

        self.assertRedirects(response, reverse("dashboard"))

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("dashboard"))

        self.assertRedirects(response, f'{reverse("login")}?next={reverse("dashboard")}')

    def test_authenticated_user_can_access_dashboard(self):
        user = get_user_model().objects.create_user(
            username="samantha",
            email="samantha@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Elarion Dashboard")


class TestSignupFlow(TestCase):
    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create account")
        self.assertContains(response, "username")

    def test_valid_signup_creates_account_and_redirects_to_login(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "new_player",
                "email": "new_player@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertRedirects(response, f'{reverse("login")}?created=1')
        self.assertTrue(get_user_model().objects.filter(username="new_player").exists())

    def test_invalid_signup_shows_errors_and_does_not_create_user(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "bad_signup",
                "email": "bad_signup@example.com",
                "password1": "StrongPass123!",
                "password2": "DifferentPass456!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields")
        self.assertFalse(get_user_model().objects.filter(username="bad_signup").exists())

    def test_authenticated_user_is_redirected_from_signup_to_dashboard(self):
        user = get_user_model().objects.create_user(
            username="already_here",
            email="already_here@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("signup"))

        self.assertRedirects(response, reverse("dashboard"))


class TestLoginFlow(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="login_user",
            email="login_user@example.com",
            password="StrongPass123!",
        )

    def test_valid_login_creates_session_and_redirects(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "login_user",
                "password": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("dashboard"))

        dashboard = self.client.get(reverse("dashboard"))
        self.assertEqual(dashboard.status_code, 200)

    def test_invalid_login_shows_non_revealing_error(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "login_user",
                "password": "WrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

        dashboard = self.client.get(reverse("dashboard"))
        self.assertRedirects(dashboard, f'{reverse("login")}?next={reverse("dashboard")}')

    def test_login_post_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)

        login_page = csrf_client.get(reverse("login"))
        self.assertContains(login_page, "csrfmiddlewaretoken")

        blocked = csrf_client.post(
            reverse("login"),
            {
                "username": "login_user",
                "password": "StrongPass123!",
            },
        )
        self.assertEqual(blocked.status_code, 403)


class TestLoginSecurity(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="secure_user",
            email="secure_user@example.com",
            password="StrongPass123!",
        )
        cache.clear()

    def tearDown(self):
        cache.clear()

    @override_settings(LOGIN_RATE_LIMIT_ATTEMPTS=2, LOGIN_RATE_LIMIT_WINDOW_SECONDS=60)
    def test_login_is_rate_limited_after_repeated_failures(self):
        bad_payload = {"username": "secure_user", "password": "WrongPassword123!"}

        self.client.post(reverse("login"), bad_payload)
        self.client.post(reverse("login"), bad_payload)
        blocked_response = self.client.post(reverse("login"), bad_payload)

        self.assertEqual(blocked_response.status_code, 429)
        self.assertContains(
            blocked_response,
            "Too many failed login attempts",
            status_code=429,
        )

    @override_settings(LOGIN_RATE_LIMIT_ATTEMPTS=2, LOGIN_RATE_LIMIT_WINDOW_SECONDS=60)
    def test_successful_login_resets_rate_limit_counter(self):
        bad_payload = {"username": "secure_user", "password": "WrongPassword123!"}
        good_payload = {"username": "secure_user", "password": "StrongPass123!"}

        self.client.post(reverse("login"), bad_payload)
        good_response = self.client.post(reverse("login"), good_payload)
        next_bad_response = self.client.post(reverse("login"), bad_payload)

        self.assertEqual(good_response.status_code, 302)
        self.assertEqual(next_bad_response.status_code, 200)

    def test_failed_login_is_logged(self):
        bad_payload = {"username": "secure_user", "password": "WrongPassword123!"}

        with self.assertLogs("apps.core.auth", level="WARNING") as captured:
            self.client.post(reverse("login"), bad_payload)

        self.assertTrue(any("login_failed" in message for message in captured.output))


class TestLogoutFlow(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="logout_user",
            email="logout_user@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(self.user)

    def test_logout_get_is_not_allowed(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)

    def test_logout_post_redirects_home_with_confirmation_message(self):
        response = self.client.post(reverse("logout"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are now logged out.")

    def test_logout_ends_session_and_blocks_protected_route(self):
        self.client.post(reverse("logout"))

        dashboard_response = self.client.get(reverse("dashboard"))
        self.assertRedirects(
            dashboard_response,
            f'{reverse("login")}?next={reverse("dashboard")}',
        )

    def test_logout_event_is_logged(self):
        with self.assertLogs("apps.core.auth", level="INFO") as captured:
            self.client.post(reverse("logout"))

        self.assertTrue(any("logout username=logout_user" in message for message in captured.output))


class TestBootstrapDevDbCommand(SimpleTestCase):
    @patch("apps.core.management.commands.bootstrap_dev_db.call_command")
    def test_bootstrap_dev_db_creates_parent_dir_and_runs_migrate(self, mock_call_command):
        with TemporaryDirectory() as tempdir:
            db_path = Path(tempdir) / "nested" / "elarion.sqlite3"

            with override_settings(
                DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": str(db_path)}}
            ):
                stdout = StringIO()
                call_command("bootstrap_dev_db", stdout=stdout)
                self.assertTrue(db_path.parent.exists())

        mock_call_command.assert_called_once_with("migrate", interactive=False, verbosity=1)

    @patch("apps.core.management.commands.bootstrap_dev_db.call_command")
    def test_bootstrap_dev_db_is_idempotent(self, mock_call_command):
        with TemporaryDirectory() as tempdir:
            db_path = Path(tempdir) / "nested" / "elarion.sqlite3"
            db_settings = {
                "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": str(db_path)}
            }

            with override_settings(DATABASES=db_settings):
                call_command("bootstrap_dev_db")
                call_command("bootstrap_dev_db")
                self.assertTrue(db_path.parent.exists())

        self.assertEqual(mock_call_command.call_count, 2)


class TestSeedDevDataCommand(TestCase):
    def test_seed_dev_data_is_idempotent(self):
        call_command("seed_dev_data")
        call_command("seed_dev_data")

        user_model = get_user_model()
        self.assertEqual(
            user_model.objects.filter(username__in=[entry["username"] for entry in SEED_USERS]).count(),
            len(SEED_USERS),
        )

    def test_seed_dev_data_reset_recreates_seed_records(self):
        call_command("seed_dev_data")
        user_model = get_user_model()
        gm = user_model.objects.get(username="gm_samantha")
        gm.email = "old@example.com"
        gm.save(update_fields=["email"])

        call_command("seed_dev_data", reset=True)

        gm = user_model.objects.get(username="gm_samantha")
        self.assertEqual(gm.email, "gm_samantha@example.com")
        self.assertEqual(
            user_model.objects.filter(username__in=[entry["username"] for entry in SEED_USERS]).count(),
            len(SEED_USERS),
        )


class TestCoreModelConstraints(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="gm_owner",
            email="gm_owner@example.com",
            password="StrongPass123!",
        )
        self.rules = RulesSystem.objects.create(code="dnd5e-2024", name="D&D 5e", edition="2024")
        self.world = World.objects.create(
            name="Sable Reach", slug="sable-reach", rules_system=self.rules, gm=self.user
        )

    def test_campaign_name_must_be_unique_within_world(self):
        Campaign.objects.create(world=self.world, name="Ashen Crown", slug="ashen-crown")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Campaign.objects.create(world=self.world, name="Ashen Crown", slug="ashen-crown-2")

    def test_character_name_must_be_unique_per_owner_per_world(self):
        Character.objects.create(
            world=self.world,
            owner=self.user,
            name="Ari Voss",
            class_name="Ranger",
            race_name="Human",
            level=4,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Character.objects.create(
                    world=self.world,
                    owner=self.user,
                    name="Ari Voss",
                    class_name="Ranger",
                    race_name="Human",
                    level=4,
                )

    def test_world_delete_cascades_campaigns_and_characters(self):
        campaign = Campaign.objects.create(world=self.world, name="Ashen Crown", slug="ashen-crown")
        character = Character.objects.create(
            world=self.world,
            owner=self.user,
            name="Ari Voss",
            class_name="Ranger",
            race_name="Human",
            level=4,
        )
        CampaignCharacter.objects.create(campaign=campaign, character=character)

        self.world.delete()

        self.assertEqual(Campaign.objects.count(), 0)
        self.assertEqual(Character.objects.count(), 0)
        self.assertEqual(CampaignCharacter.objects.count(), 0)

    def test_rules_system_delete_is_protected_when_world_exists(self):
        with self.assertRaises(ProtectedError):
            self.rules.delete()


class TestWorldImportFromSrd(TestCase):
    def setUp(self):
        self.gm = get_user_model().objects.create_user(
            username="world_gm",
            email="world_gm@example.com",
            password="StrongPass123!",
        )
        call_command("seed_srd_baseline")

    def test_seed_srd_baseline_contains_requested_focus_entities(self):
        self.assertEqual(
            set(BaselineSpecies.objects.values_list("name", flat=True)),
            {"Human", "Elf", "Dwarf"},
        )
        self.assertEqual(
            set(BaselineClass.objects.values_list("name", flat=True)),
            {"Fighter", "Cleric", "Magic User", "Thief"},
        )
        self.assertTrue(BaselineItem.objects.filter(name="Longsword").exists())
        self.assertTrue(BaselineItem.objects.filter(name="Thieves' Tools").exists())

    def test_create_world_imports_only_selected_groups(self):
        call_command(
            "create_world_from_srd",
            world_name="Focused World",
            world_slug="focused-world",
            gm_username=self.gm.username,
            include="species,classes",
        )
        world = World.objects.get(slug="focused-world")

        self.assertEqual(WorldSpecies.objects.filter(world=world).count(), 3)
        self.assertEqual(WorldClass.objects.filter(world=world).count(), 4)
        self.assertEqual(WorldSpell.objects.filter(world=world).count(), 0)
        self.assertEqual(WorldItem.objects.filter(world=world).count(), 0)

    def test_create_world_with_spells_copies_progression_table(self):
        call_command(
            "create_world_from_srd",
            world_name="Spell World",
            world_slug="spell-world",
            gm_username=self.gm.username,
            include="classes,spells",
        )
        world = World.objects.get(slug="spell-world")

        self.assertGreater(WorldSpell.objects.filter(world=world).count(), 0)
        self.assertGreater(WorldClassSpellProgression.objects.filter(world=world).count(), 0)
        self.assertEqual(WorldSpecies.objects.filter(world=world).count(), 0)

    def test_spells_without_classes_is_rejected(self):
        with self.assertRaisesMessage(
            ValueError,
            "Including spells requires including classes",
        ):
            call_command(
                "create_world_from_srd",
                world_name="Invalid World",
                world_slug="invalid-world",
                gm_username=self.gm.username,
                include="spells",
            )
