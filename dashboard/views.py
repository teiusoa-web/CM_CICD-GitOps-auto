from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone

from tickets.models import Ticket


@login_required
def index(request):
    if not (request.user.is_admin_role() or request.user.is_agent()):
        return HttpResponseForbidden("Dashboard dành cho Agent và Admin.")

    qs = Ticket.objects.all()
    now = timezone.now()
    open_statuses = [
        Ticket.Status.NEW,
        Ticket.Status.ASSIGNED,
        Ticket.Status.IN_PROGRESS,
    ]
    overdue = qs.filter(status__in=open_statuses, due_at__lt=now)

    by_status = [
        (label, qs.filter(status=value).count()) for value, label in Ticket.Status.choices
    ]
    by_priority = [
        (label, qs.filter(priority=value).count()) for value, label in Ticket.Priority.choices
    ]

    context = {
        "total": qs.count(),
        "new_count": qs.filter(status=Ticket.Status.NEW).count(),
        "in_progress_count": qs.filter(
            status__in=[Ticket.Status.ASSIGNED, Ticket.Status.IN_PROGRESS]
        ).count(),
        "resolved_count": qs.filter(status=Ticket.Status.RESOLVED).count(),
        "overdue_count": overdue.count(),
        "by_status": by_status,
        "by_priority": by_priority,
        "overdue_tickets": overdue.select_related("created_by", "assigned_to")[:10],
    }
    return render(request, "dashboard/index.html", context)
