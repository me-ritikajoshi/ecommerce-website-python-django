from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AdminDashboardTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="admin-pass-123",
            is_staff=True,
        )

    def test_admin_dashboard_requires_authentication(self):
        response = self.client.get(reverse("adminpage:dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_accessible_for_staff(self):
        self.client.login(username="admin", password="admin-pass-123")
        response = self.client.get(reverse("adminpage:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Dashboard")
