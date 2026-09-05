from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from tickets.forms import (
    CommentForm,
    TicketAssignForm,
    TicketContentForm,
    TicketCreateForm,
    TicketWorkflowForm,
)
from tickets.models import Ticket
from tickets.permissions import (
    can_assign,
    can_change_workflow,
    can_claim,
    can_close,
    can_comment,
    can_edit_content,
    can_view_ticket,
    visible_tickets,
)


@login_required
def ticket_list(request):
    tickets = visible_tickets(request.user)
    status = request.GET.get("status")
    if status:
        tickets = tickets.filter(status=status)
    return render(
        request,
        "tickets/list.html",
        {"tickets": tickets, "statuses": Ticket.Status.choices, "current_status": status},
    )


@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.due_at = timezone.now() + timedelta(days=7)
            ticket.save()
            messages.success(request, "Đã tạo ticket.")
            return redirect("tickets:detail", pk=ticket.pk)
    else:
        form = TicketCreateForm()
    return render(request, "tickets/form.html", {"form": form, "title": "Tạo ticket"})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket.objects.select_related("created_by", "assigned_to"), pk=pk)
    if not can_view_ticket(request.user, ticket):
        return HttpResponseForbidden("Bạn không có quyền xem ticket này.")

    comment_form = CommentForm()
    if request.method == "POST" and "add_comment" in request.POST:
        if not can_comment(request.user, ticket):
            return HttpResponseForbidden("Không thể bình luận trên ticket này.")
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, "Đã thêm bình luận.")
            return redirect("tickets:detail", pk=ticket.pk)

    assign_form = None
    if can_assign(request.user):
        assign_form = TicketAssignForm(initial={"assigned_to": ticket.assigned_to_id})

    workflow_form = None
    if can_change_workflow(request.user, ticket):
        workflow_form = TicketWorkflowForm(instance=ticket)

    return render(
        request,
        "tickets/detail.html",
        {
            "ticket": ticket,
            "comments": ticket.comments.select_related("author"),
            "comment_form": comment_form,
            "assign_form": assign_form,
            "workflow_form": workflow_form,
            "can_edit": can_edit_content(request.user, ticket),
            "can_workflow": can_change_workflow(request.user, ticket),
            "can_claim_ticket": can_claim(request.user, ticket),
            "can_close_ticket": can_close(request.user, ticket),
            "can_assign_ticket": can_assign(request.user),
            "can_add_comment": can_comment(request.user, ticket),
        },
    )


@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not can_edit_content(request.user, ticket):
        return HttpResponseForbidden("Bạn không thể sửa nội dung ticket này.")
    if request.method == "POST":
        form = TicketContentForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Đã cập nhật ticket.")
            return redirect("tickets:detail", pk=ticket.pk)
    else:
        form = TicketContentForm(instance=ticket)
    return render(request, "tickets/form.html", {"form": form, "title": "Cập nhật ticket"})


@login_required
@require_POST
def ticket_workflow(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not can_change_workflow(request.user, ticket):
        return HttpResponseForbidden("Bạn không thể đổi trạng thái ticket này.")
    form = TicketWorkflowForm(request.POST, instance=ticket)
    if form.is_valid():
        form.save()
        messages.success(request, "Đã cập nhật trạng thái / ưu tiên.")
    else:
        messages.error(request, "Dữ liệu không hợp lệ.")
    return redirect("tickets:detail", pk=ticket.pk)


@login_required
@require_POST
def ticket_claim(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not can_claim(request.user, ticket):
        return HttpResponseForbidden("Không thể nhận ticket này.")
    ticket.assigned_to = request.user
    ticket.status = Ticket.Status.ASSIGNED
    ticket.save()
    messages.success(request, "Bạn đã nhận ticket.")
    return redirect("tickets:detail", pk=ticket.pk)


@login_required
@require_POST
def ticket_assign(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not can_assign(request.user):
        return HttpResponseForbidden("Chỉ admin mới được phân công.")
    form = TicketAssignForm(request.POST)
    if form.is_valid():
        agent = form.cleaned_data["assigned_to"]
        ticket.assigned_to = agent
        if agent and ticket.status == Ticket.Status.NEW:
            ticket.status = Ticket.Status.ASSIGNED
        if agent is None and ticket.status == Ticket.Status.ASSIGNED:
            ticket.status = Ticket.Status.NEW
        ticket.save()
        messages.success(request, "Đã cập nhật phân công.")
    return redirect("tickets:detail", pk=ticket.pk)


@login_required
@require_POST
def ticket_close(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not can_close(request.user, ticket):
        return HttpResponseForbidden("Không thể đóng ticket này.")
    ticket.status = Ticket.Status.CLOSED
    ticket.save()
    messages.success(request, "Đã đóng ticket.")
    return redirect("tickets:detail", pk=ticket.pk)
