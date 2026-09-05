from django.urls import path

from tickets import views

app_name = "tickets"

urlpatterns = [
    path("", views.ticket_list, name="list"),
    path("new/", views.ticket_create, name="create"),
    path("<int:pk>/", views.ticket_detail, name="detail"),
    path("<int:pk>/edit/", views.ticket_update, name="update"),
    path("<int:pk>/workflow/", views.ticket_workflow, name="workflow"),
    path("<int:pk>/claim/", views.ticket_claim, name="claim"),
    path("<int:pk>/assign/", views.ticket_assign, name="assign"),
    path("<int:pk>/close/", views.ticket_close, name="close"),
]
