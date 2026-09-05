from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

DEMO_PASSWORD = "Devdesk-demo-1"


class Command(BaseCommand):
    help = "Create demo users admin / agent / customer (password: Devdesk-demo-1)."

    def handle(self, *args, **options):
        specs = [
            ("admin", User.Role.ADMIN, True),
            ("agent", User.Role.AGENT, False),
            ("customer", User.Role.CUSTOMER, False),
        ]
        for username, role, is_staff in specs:
            user, created = User.objects.get_or_create(username=username)
            user.role = role
            user.is_staff = is_staff
            user.is_superuser = is_staff
            user.set_password(DEMO_PASSWORD)
            user.save()
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} {username} ({role})")
        self.stdout.write(self.style.SUCCESS(f"Password for all demo users: {DEMO_PASSWORD}"))
