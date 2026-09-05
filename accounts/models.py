from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        AGENT = "agent", "Agent"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
        db_index=True,
    )

    def is_customer(self) -> bool:
        return self.role == self.Role.CUSTOMER

    def is_agent(self) -> bool:
        return self.role == self.Role.AGENT

    def is_admin_role(self) -> bool:
        return self.role == self.Role.ADMIN or self.is_superuser
