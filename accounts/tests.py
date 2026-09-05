from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_with_default_customer_role(self):
        user = User.objects.create_user(username="alice", password="secret-pass-123")
        self.assertEqual(user.role, User.Role.CUSTOMER)
        self.assertTrue(user.is_customer())
        self.assertFalse(user.is_agent())
        self.assertFalse(user.is_admin_role())

    def test_create_agent_and_admin_roles(self):
        agent = User.objects.create_user(
            username="bob",
            password="secret-pass-123",
            role=User.Role.AGENT,
        )
        admin = User.objects.create_user(
            username="carol",
            password="secret-pass-123",
            role=User.Role.ADMIN,
        )
        self.assertTrue(agent.is_agent())
        self.assertTrue(admin.is_admin_role())


class AuthenticationTests(TestCase):
    def test_home_redirects_anonymous_to_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_register_creates_customer_and_logs_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "secret-pass-123",
                "password2": "secret-pass-123",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="newuser")
        self.assertEqual(user.role, User.Role.CUSTOMER)

    def test_login_logout(self):
        User.objects.create_user(username="dave", password="secret-pass-123")
        logged_in = self.client.login(username="dave", password="secret-pass-123")
        self.assertTrue(logged_in)
        response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)

    def test_customer_cannot_manage_users(self):
        User.objects.create_user(username="erin", password="secret-pass-123")
        self.client.login(username="erin", password="secret-pass-123")
        response = self.client.get(reverse("accounts:users"))
        self.assertEqual(response.status_code, 403)
