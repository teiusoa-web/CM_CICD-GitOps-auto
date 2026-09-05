from django import forms
from django.contrib.auth import get_user_model

from tickets.models import Comment, Ticket

User = get_user_model()


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "priority")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "priority": forms.Select(attrs={"class": "form-select"}),
        }


class TicketContentForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "priority")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "priority": forms.Select(attrs={"class": "form-select"}),
        }


class TicketWorkflowForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("status", "priority")
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
        }


class TicketAssignForm(forms.Form):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.Role.AGENT),
        required=False,
        empty_label="— Chưa phân công —",
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Agent",
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Thêm bình luận..."}
            ),
        }
        labels = {"body": ""}
