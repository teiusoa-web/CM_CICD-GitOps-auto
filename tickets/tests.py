from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tickets.models import Comment, Ticket

User = get_user_model()


class TicketModelTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer1",
            password="secret-pass-123",
            role=User.Role.CUSTOMER,
        )
        self.agent = User.objects.create_user(
            username="agent1",
            password="secret-pass-123",
            role=User.Role.AGENT,
        )

    def test_create_ticket(self):
        ticket = Ticket.objects.create(
            title="Cannot login",
            description="Password reset loop",
            created_by=self.customer,
        )
        self.assertEqual(ticket.status, Ticket.Status.NEW)
        self.assertEqual(ticket.priority, Ticket.Priority.MEDIUM)
        self.assertIsNone(ticket.assigned_to)
        self.assertIsNone(ticket.resolved_at)

    def test_resolved_at_set_when_status_resolved(self):
        ticket = Ticket.objects.create(
            title="Printer jam",
            description="Office printer stuck",
            created_by=self.customer,
            assigned_to=self.agent,
            status=Ticket.Status.IN_PROGRESS,
        )
        ticket.status = Ticket.Status.RESOLVED
        ticket.save()
        ticket.refresh_from_db()
        self.assertIsNotNone(ticket.resolved_at)

    def test_comment_on_ticket(self):
        ticket = Ticket.objects.create(
            title="VPN down",
            description="Cannot reach office network",
            created_by=self.customer,
        )
        comment = Comment.objects.create(
            ticket=ticket,
            author=self.agent,
            body="Looking into this now.",
        )
        self.assertEqual(ticket.comments.count(), 1)
        self.assertEqual(comment.author, self.agent)


class HealthCheckTests(TestCase):
    def test_health_returns_ok(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")


class TicketPermissionTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            username="customer1",
            password="secret-pass-123",
            role=User.Role.CUSTOMER,
        )
        self.other = User.objects.create_user(
            username="other",
            password="secret-pass-123",
            role=User.Role.CUSTOMER,
        )
        self.agent = User.objects.create_user(
            username="agent1",
            password="secret-pass-123",
            role=User.Role.AGENT,
        )
        self.admin = User.objects.create_user(
            username="admin1",
            password="secret-pass-123",
            role=User.Role.ADMIN,
        )
        self.ticket = Ticket.objects.create(
            title="Laptop issue",
            description="Won't boot",
            created_by=self.customer,
        )

    def test_create_ticket_via_form(self):
        self.client.login(username="customer1", password="secret-pass-123")
        response = self.client.post(
            reverse("tickets:create"),
            {
                "title": "WiFi down",
                "description": "No internet on floor 3",
                "priority": Ticket.Priority.HIGH,
            },
        )
        self.assertEqual(response.status_code, 302)
        created = Ticket.objects.get(title="WiFi down")
        self.assertEqual(created.created_by, self.customer)
        self.assertEqual(created.status, Ticket.Status.NEW)

    def test_customer_cannot_view_other_ticket(self):
        self.client.login(username="other", password="secret-pass-123")
        response = self.client.get(reverse("tickets:detail", args=[self.ticket.pk]))
        self.assertEqual(response.status_code, 403)

    def test_agent_claims_and_changes_status(self):
        self.client.login(username="agent1", password="secret-pass-123")
        claim = self.client.post(reverse("tickets:claim", args=[self.ticket.pk]))
        self.assertEqual(claim.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.assigned_to, self.agent)
        self.assertEqual(self.ticket.status, Ticket.Status.ASSIGNED)

        workflow = self.client.post(
            reverse("tickets:workflow", args=[self.ticket.pk]),
            {"status": Ticket.Status.IN_PROGRESS, "priority": Ticket.Priority.HIGH},
        )
        self.assertEqual(workflow.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.IN_PROGRESS)
        self.assertEqual(self.ticket.priority, Ticket.Priority.HIGH)

    def test_comment_via_form(self):
        self.client.login(username="customer1", password="secret-pass-123")
        response = self.client.post(
            reverse("tickets:detail", args=[self.ticket.pk]),
            {"add_comment": "1", "body": "Any update?"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.ticket.comments.filter(body="Any update?").exists())

    def test_admin_assigns_agent(self):
        self.client.login(username="admin1", password="secret-pass-123")
        response = self.client.post(
            reverse("tickets:assign", args=[self.ticket.pk]),
            {"assigned_to": self.agent.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.assigned_to, self.agent)
        self.assertEqual(self.ticket.status, Ticket.Status.ASSIGNED)

    def test_customer_closes_own_ticket(self):
        self.client.login(username="customer1", password="secret-pass-123")
        response = self.client.post(reverse("tickets:close", args=[self.ticket.pk]))
        self.assertEqual(response.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.CLOSED)
