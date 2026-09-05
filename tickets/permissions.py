from django.db.models import Q

from tickets.models import Ticket


def visible_tickets(user):
    qs = Ticket.objects.select_related("created_by", "assigned_to")
    if user.is_admin_role():
        return qs
    if user.is_agent():
        return qs.filter(Q(assigned_to=user) | Q(assigned_to__isnull=True))
    return qs.filter(created_by=user)


def can_view_ticket(user, ticket) -> bool:
    return visible_tickets(user).filter(pk=ticket.pk).exists()


def can_edit_content(user, ticket) -> bool:
    if ticket.status == Ticket.Status.CLOSED:
        return False
    if user.is_admin_role():
        return True
    return user.is_customer() and ticket.created_by_id == user.id


def can_change_workflow(user, ticket) -> bool:
    if user.is_admin_role():
        return True
    return user.is_agent() and ticket.assigned_to_id == user.id


def can_claim(user, ticket) -> bool:
    return (
        user.is_agent()
        and ticket.assigned_to_id is None
        and ticket.status == Ticket.Status.NEW
    )


def can_assign(user) -> bool:
    return user.is_admin_role()


def can_close(user, ticket) -> bool:
    if ticket.status == Ticket.Status.CLOSED:
        return False
    if user.is_admin_role():
        return True
    if user.is_customer() and ticket.created_by_id == user.id:
        return True
    return user.is_agent() and ticket.assigned_to_id == user.id


def can_comment(user, ticket) -> bool:
    return can_view_ticket(user, ticket) and ticket.status != Ticket.Status.CLOSED
