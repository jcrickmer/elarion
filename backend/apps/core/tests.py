from django.urls import reverse
from django.test import TestCase


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
