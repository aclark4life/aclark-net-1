from .models import Client
from .models import Contact
from .models import Estimate
from .models import Invoice
from .models import Note
from .models import Profile
from .models import Project
from .models import Report
from .models import Service
from .models import Task
from .models import TaskOrder
from .models import Time
from django import forms
from django.utils import timezone


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "rate",
            "bio",
            "address",
            "job_title",
            "twitter_username",
            "page_size",
            "published",
            "avatar_url",
        )
        widgets = {"bio": forms.widgets.TextInput(attrs={"class": "tinymce"})}


class AdminTimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = (
            "date",
            "hours",
            "description",
            "estimate",
            "invoice",
            "project",
            "user",
            "task",
            "task_order",
            "invoiced",
        )
        widgets = {"hours": forms.widgets.NumberInput(attrs={"class": "col-2"})}

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            "active",
            "title",
            "first_name",
            "last_name",
            "email",
            "office_phone",
            "mobile_phone",
            "client",
            "subscribed",
        )


class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = (
            "hidden",
            "subject",
            "client",
            "project",
            "task",
            "start_date",
            "end_date",
            "accepted_date",
            "issue_date",
            "note",
        )

    issue_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )

    accepted_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )


class InvoiceForm(forms.ModelForm):
    """
    Issue Date, Last Payment Date, Invoice ID, PO Number, Client, Subject,
    Invoice Amount, Paid Amount, Balance, Subtotal, Discount, Tax, Tax2,
    Currency, Currency Symbol, Document Type
    """

    class Meta:
        model = Invoice
        fields = (
            "hidden",
            "subject",
            "po_number",
            "sa_number",
            "start_date",
            "end_date",
            "client",
            "project",
            "issue_date",
            "due_date",
            "last_payment_date",
            "note",
        )

    issue_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )

    last_payment_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "text")
        widgets = {"text": forms.widgets.TextInput(attrs={"class": "tinymce"})}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("rate", "bio", "address", "job_title", "twitter_username")
        widgets = {"bio": forms.widgets.TextInput(attrs={"class": "tinymce"})}


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "active",
            "hidden",
            "name",
            "start_date",
            "end_date",
            "client",
            "task",
            "team",
        )

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ("icon_name", "icon_size", "icon_color")

    invoices = forms.ModelMultipleChoiceField(
        required=False, queryset=Invoice.objects.all().order_by("-issue_date")
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {"description": forms.widgets.TextInput(attrs={"class": "tinymce"})}


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ("icon_name", "icon_size", "icon_color", "color")


class TaskOrderForm(forms.ModelForm):
    class Meta:
        model = TaskOrder
        fields = "__all__"


class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ("date", "project", "hours", "description")
        widgets = {"hours": forms.widgets.NumberInput(attrs={"class": "col-2"})}
