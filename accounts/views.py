from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from accounts.forms import LoginForm, RegisterForm, RoleUpdateForm
from accounts.models import User


class DevDeskLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


class DevDeskLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Tài khoản đã được tạo.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def user_list(request):
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Chỉ admin mới quản lý người dùng.")
    users = User.objects.order_by("username")
    return render(request, "accounts/user_list.html", {"users": users})


@login_required
@require_POST
def user_update_role(request, pk):
    if not request.user.is_admin_role():
        return HttpResponseForbidden("Chỉ admin mới đổi vai trò.")
    user = get_object_or_404(User, pk=pk)
    form = RoleUpdateForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, f"Đã cập nhật vai trò của {user.username}.")
    return redirect("accounts:users")
