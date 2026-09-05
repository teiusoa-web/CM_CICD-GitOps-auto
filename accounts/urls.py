from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.DevDeskLoginView.as_view(), name="login"),
    path("logout/", views.DevDeskLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("users/", views.user_list, name="users"),
    path("users/<int:pk>/role/", views.user_update_role, name="user_role"),
]
