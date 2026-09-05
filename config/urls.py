from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from config.views import health


def home(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    if request.user.is_admin_role():
        return redirect("dashboard:index")
    return redirect("tickets:list")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    path("accounts/", include("accounts.urls")),
    path("tickets/", include("tickets.urls")),
    path("dashboard/", include("dashboard.urls")),
]
