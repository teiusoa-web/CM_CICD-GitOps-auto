from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Ticket

User = get_user_model()


class DashboardTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="cust",
            password="secret-pass-123",
            role=User.Role.CUSTOMER,
        )
        self.admin = User.objects.create_user(
            username="adm",
            password="secret-pass-123",
            role=User.Role.ADMIN,
        )
        Ticket.objects.create(
            title="First",
            description="Desc",
            created_by=self.customer,
        )

    def test_customer_forbidden(self):
        self.client.login(username="cust", password="secret-pass-123")
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 403)

    def test_admin_sees_stats(self):
        self.client.login(username="adm", password="secret-pass-123")
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tổng ticket")
        self.assertEqual(response.context["total"], 1)
        self.assertEqual(response.context["new_count"], 1)
