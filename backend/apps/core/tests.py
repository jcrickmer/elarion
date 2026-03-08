from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, override_settings
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from io import StringIO
from django.core.management import call_command
from apps.core.management.commands.seed_dev_data import SEED_USERS


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
