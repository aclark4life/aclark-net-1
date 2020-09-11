from .models import Account
from .models import Client
from .models import Company
from .models import Contact
from .models import Estimate
from .models import Invoice
from .models import Note
from .models import Profile
from .models import Project
from .models import Report
from .models import Service
from .models import Task
from .models import Time
from django import forms
from django.utils import timezone


DOC_TYPES = [
    ("Invoice", "Invoice"),
    ("Estimate", "Estimate"),
    ("Proposal", "Proposal"),
    ("Statement of Work", "Statement of Work"),
    ("Task Order", "Task Order"),
    ("Independent Government Cost Estimate", "Independent Government Cost Estimate"),
]


class AdminProfileForm(forms.ModelForm):
    """
    """

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
            "notifications",
            "principal",
            "interest",
            "term",
        )
        widgets = {"bio": forms.widgets.TextInput(attrs={"class": "tinymce"})}


class AdminTimeForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Time
        fields = (
            "invoiced",
            "user",
            "date",
            "hours",
            "description",
            "quantity",
            "unit",
            "unit_price",
            "total_price",
            "estimate",
            "project",
            "task",
            "invoice",
        )
        widgets = {"hours": forms.widgets.NumberInput(attrs={"class": "col-2"})}

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )


class AccountForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Account
        exclude = ("tags", "active", "hidden")


class ClientForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Client
        exclude = ("tags", "active", "hidden", "published")


class CompanyForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Company
        fields = "__all__"


class ContactForm(forms.ModelForm):
    """
    """

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
    """
    """

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
            "ein",
            "sa_number",
            "start_date",
            "end_date",
            "client",
            "project",
            "issue_date",
            "due_date",
            "last_payment_date",
            "note",
            "doc_type",
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
    doc_type = forms.CharField(widget=forms.Select(choices=DOC_TYPES))


class NoteForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Note
        exclude = (
            "due_date",
            "active",
            "hidden",
            "tags",
        )
        widgets = {"text": forms.widgets.TextInput(attrs={"class": "tinymce"})}

    doc_type = forms.CharField(widget=forms.Select(choices=DOC_TYPES))


class ProfileForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Profile
        fields = (
            "rate",
            "bio",
            "address",
            "job_title",
            "twitter_username",
            "notifications",
        )
        widgets = {"bio": forms.widgets.TextInput(attrs={"class": "tinymce"})}


class ProjectForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Project
        exclude = (
            "active",
            "hidden",
            "tags",
            "code",
            "total_hours",
            "billable_hours",
            "amount",
            "budget",
            "budget_spent",
            "budget_remaining",
            "total_costs",
            "team_costs",
            "cost",
            "expenses",
        )


class ReportForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Report
        exclude = ("icon_name", "icon_size", "icon_color", "hidden")

    invoices = forms.ModelMultipleChoiceField(
        required=False, queryset=Invoice.objects.all().order_by("-issue_date")
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2"}),
        required=False,
        initial=timezone.now(),
    )


class ServiceForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Service
        fields = "__all__"
        widgets = {"description": forms.widgets.TextInput(attrs={"class": "tinymce"})}


class TaskForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Task
        exclude = ("icon_name", "icon_size", "icon_color", "color")


class TimeForm(forms.ModelForm):
    """
    """

    class Meta:
        model = Time
        fields = ("date", "project", "hours", "description")
        widgets = {"hours": forms.widgets.NumberInput(attrs={"class": "col-2"})}
