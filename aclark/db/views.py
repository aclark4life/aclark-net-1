from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.text import slugify
from rest_framework import viewsets
from .forms import AccountForm
from .forms import AdminProfileForm
from .forms import AdminTimeForm
from .forms import ClientForm
from .forms import CompanyForm
from .forms import ContactForm
from .forms import EstimateForm
from .forms import InvoiceForm
from .forms import NoteForm
from .forms import ProfileForm
from .forms import ProjectForm
from .forms import ReportForm
from .forms import ServiceForm
from .forms import TaskForm
from .forms import TimeForm
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
from .models import SiteConfiguration
from .models import Testimonial
from .models import Task
from .models import Time
from .export import render_doc
from .export import render_pdf
from .export import render_xls
from .igce import render_xls as render_xls_igce
from .mail import mail_send
from .misc import has_profile
from .plot import get_plot
from .serializers import ClientSerializer
from .serializers import TestimonialSerializer
from .edit import edit
from .utils import get_index_items
from .utils import get_page_items

FOUR_O_3 = "Sorry, you are not allowed to see that."


class ClientViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Client.objects.filter(published=True).order_by("name")
    serializer_class = ClientSerializer


class TestimonialViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Testimonial.objects.filter(active=True).order_by("-issue_date")
    serializer_class = TestimonialSerializer


@staff_member_required
def account_view(request, pk=None):
    """
    """

    order_by = {
        "contact": ("-active",),
        "project": ("-updated",),
        "estimate": ("-issue_date",),
        "invoice": ("-issue_date",),
    }
    context = get_page_items(
        contact_model=Contact,
        invoice_model=Invoice,
        estimate_model=Estimate,
        note_model=Note,
        model=Account,
        order_by=order_by,
        pk=pk,
        project_model=Project,
        report_model=Report,
        request=request,
    )
    return render(request, "account_view.html", context)


@staff_member_required
def account_edit(request, pk=None):
    """
    """

    return edit(
        request, report_model=Report, form_model=AccountForm, model=Account, pk=pk
    )


@staff_member_required
def account_index(request):
    """
    """

    context = get_index_items(
        model=Account,
        report_model=Report,
        order_by=("-active", "name"),
        request=request,
        search_fields=("name",),
    )
    return render(request, "account_index.html", context)


@staff_member_required
def client_view(request, pk=None):
    """
    """

    order_by = {
        "contact": ("-active",),
        "project": ("-updated",),
        "estimate": ("-issue_date",),
        "invoice": ("-issue_date",),
    }
    context = get_page_items(
        contact_model=Contact,
        invoice_model=Invoice,
        estimate_model=Estimate,
        note_model=Note,
        model=Client,
        order_by=order_by,
        pk=pk,
        project_model=Project,
        report_model=Report,
        request=request,
    )
    return render(request, "client_view.html", context)


@staff_member_required
def client_edit(request, pk=None):
    """
    """

    return edit(
        request, report_model=Report, form_model=ClientForm, model=Client, pk=pk
    )


@staff_member_required
def client_index(request):
    """
    """

    context = get_index_items(
        model=Client,
        report_model=Report,
        order_by=("-active", "name"),
        request=request,
        search_fields=("address", "name"),
    )
    return render(request, "client_index.html", context)


def competency(request):
    """
    """

    context = get_page_items(
        site_config_model=SiteConfiguration,
        request=request,
        client_model=Client,
        service_model=Service,
    )
    if context["pdf"]:
        filename = "%s-%s.pdf" % (context["company_name"], "competency")
        return render_pdf(context, filename=filename, template="competency.html")
    return render(request, "competency_view.html", context)


@staff_member_required
def company_edit(request, pk=None):
    """
    """

    return edit(request, form_model=CompanyForm, model=Company, pk=pk)


@staff_member_required
def company_index(request):
    """
    """

    context = get_index_items(
        model=Company,
        report_model=Report,
        order_by=("-active", "name"),
        request=request,
        search_fields=("name",),
    )
    return render(request, "company_index.html", context)


@staff_member_required
def company_view(request, pk=None):
    """
    """

    context = get_page_items(model=Company, pk=pk, request=request, report_model=Report)
    return render(request, "company_view.html", context)


@staff_member_required
def contact_view(request, pk=None):
    """
    """

    context = get_page_items(
        model=Contact,
        pk=pk,
        request=request,
        report_model=Report,
        include_fields=("first_name", "last_name"),
    )
    return render(request, "contact_view.html", context)


@staff_member_required
def contact_edit(request, pk=None):
    """
    """

    return edit(
        request,
        report_model=Report,
        form_model=ContactForm,
        model=Contact,
        client_model=Client,
        user_model=User,
        pk=pk,
    )


@staff_member_required
def contact_index(request):
    """
    """

    context = get_index_items(
        model=Contact,
        report_model=Report,
        order_by=("-active", "last_name", "first_name"),
        request=request,
        search_fields=("first_name", "last_name", "email", "pk"),
    )
    return render(request, "contact_index.html", context)


def error(request):
    """
    """
    raise


@staff_member_required
def estimate_view(request, pk=None):
    """
    """

    context = get_page_items(
        model=Estimate,
        site_config_model=SiteConfiguration,
        order_by={"time": ("date", "updated")},  # For time entries
        pk=pk,
        project_model=Project,
        report_model=Report,
        time_model=Time,
        request=request,
    )
    if context["pdf"]:
        filename = "%s-%s-%s.pdf" % (context["company_name"], "estimate", pk)
        return render_pdf(context, filename=filename, template="invoice.html")
    else:
        return render(request, "estimate_view.html", context)


@staff_member_required
def estimate_edit(request, pk=None):
    """
    """

    return edit(
        request,
        form_model=EstimateForm,
        report_model=Report,
        model=Estimate,
        project_model=Project,
        client_model=Client,
        pk=pk,
        user_model=User,
    )


@staff_member_required
def estimate_index(request):
    """
    """

    context = get_index_items(
        model=Estimate,
        report_model=Report,
        order_by=("-issue_date",),
        search_fields=("subject", "amount"),
        request=request,
    )
    return render(request, "estimate_index.html", context)


@login_required
def home(request):
    """
    """

    if request.user.is_staff:
        filter_by = {"time": {"estimate": None, "invoiced": False}}
    else:
        filter_by = {
            "time": {"estimate": None, "user": request.user, "invoiced": False}
        }
    order_by = {
        "invoice": ("-issue_date",),
        "project": ("-updated",),
        "time": ("date", "updated"),
    }
    context = get_page_items(
        time_model=Time,
        invoice_model=Invoice,
        project_model=Project,
        report_model=Report,
        filter_by=filter_by,
        order_by=order_by,
        request=request,
        home_nav=True,
    )
    return render(request, "dashboard.html", context)


@staff_member_required
def invoice_view(request, pk=None):
    """
    """

    context = get_page_items(
        model=Invoice,
        site_config_model=SiteConfiguration,
        order_by={"time": ("date", "updated")},  # For time entries
        pk=pk,
        request=request,
        time_model=Time,
        report_model=Report,
    )
    filename = "%s-%s-%s" % (context["company_name"], "invoice", pk)
    if context["pdf"]:
        filename = ".".join((filename, "pdf"))
        return render_pdf(context, filename=filename, template="invoice.html")
    elif context["xls"]:
        filename = ".".join((filename, "xlsx"))
        if context["doc_type"] == "Independent Government Cost Estimate":
            return render_xls_igce(context, filename=filename, template="invoice.html")
        else:
            return render_xls(context, filename=filename, template="invoice.html")
    else:
        return render(request, "invoice_view.html", context)


@staff_member_required
def invoice_edit(request, pk=None):
    """
    """

    return edit(
        request,
        report_model=Report,
        form_model=InvoiceForm,
        model=Invoice,
        client_model=Client,
        project_model=Project,
        pk=pk,
    )


@staff_member_required
def invoice_index(request):
    """
    """

    search_fields = (
        "client__name",
        "id",
        "issue_date",
        "project__name",
        "subject",
        "amount",
    )
    context = get_index_items(
        model=Invoice,
        report_model=Report,
        order_by=("-last_payment_date", "subject"),
        request=request,
        search_fields=search_fields,
    )
    return render(request, "invoice_index.html", context)


def login(request):
    """
    """

    context = {}
    context["login"] = True
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # https://stackoverflow.com/a/39316967/185820
            auth_login(request, user)
            messages.add_message(request, messages.INFO, "Login succeeded")
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.add_message(request, messages.WARNING, "Login failed")
            return HttpResponseRedirect(reverse("home"))
    return render(request, "login.html", context)


def logout(request):
    """
    """

    auth_logout(request)
    # Redirect to a success page.
    messages.add_message(request, messages.INFO, "Logout succeeded")
    return HttpResponseRedirect(reverse("home"))


@staff_member_required
def note_view(request, pk=None):
    """
    """

    context = get_page_items(
        model=Note,
        pk=pk,
        request=request,
        report_model=Report,
        site_config_model=SiteConfiguration,
        include_fields=("created", "updated", "text", "title"),
    )
    item = context["item"]
    if item.title:
        note_title = item.title
        note_title = slugify(note_title)
        filename = "%s-%s" % (context["company_name"], note_title)
    else:
        filename = "%s-%s-%s" % (context["company_name"], "note", pk)
        item.title = "Title"
    if context["mail"]:
        message = context["message"]
        subject = context["subject"]
        mail_send(html_message=message, subject=subject)
        messages.add_message(request, messages.INFO, "Note sent")
        return render(request, "note_view.html", context)
    elif context["pdf"]:
        filename = ".".join((filename, "pdf"))
        return render_pdf(context, filename=filename, template="note.html")
    elif context["doc"]:
        filename = ".".join((filename, "doc"))
        return render_doc(context, filename=filename, template="note.html")
    return render(request, "note_view.html", context)


@staff_member_required
def note_edit(request, pk=None):
    """
    """

    return edit(
        request,
        report_model=Report,
        form_model=NoteForm,
        model=Note,
        client_model=Client,
        invoice_model=Invoice,
        account_model=Account,
        pk=pk,
    )


@staff_member_required
def note_index(request, pk=None):
    """
    """

    context = get_index_items(
        model=Note,
        report_model=Report,
        order_by=("-created",),
        request=request,
        search_fields=("text", "title"),
    )
    return render(request, "note_index.html", context)


@staff_member_required
def plot(request):
    """
    """

    return get_plot(request)


@staff_member_required
def project_view(request, pk=None):
    """
    """

    context = get_page_items(
        model=Project,
        contact_model=Contact,
        estimate_model=Estimate,
        invoice_model=Invoice,
        note_model=Note,
        user_model=User,
        order_by={
            "time": ("-date",),
            "invoice": ("-issue_date",),
            "estimate": ("-issue_date",),
        },
        time_model=Time,
        pk=pk,
        request=request,
    )
    return render(request, "project_view.html", context)


@staff_member_required
def project_edit(request, pk=None):
    """
    """

    return edit(
        request,
        report_model=Report,
        form_model=ProjectForm,
        model=Project,
        client_model=Client,
        pk=pk,
    )


@staff_member_required
def project_index(request, pk=None):
    """
    """

    context = get_index_items(
        model=Project,
        report_model=Report,
        order_by=("-active", "-created"),
        request=request,
        search_fields=("id", "name"),
    )
    return render(request, "project_index.html", context)


@staff_member_required
def report_view(request, pk=None):
    """
    """

    context = get_page_items(model=Report, pk=pk, request=request)
    if context["mail"]:
        message = context["message"]
        subject = context["subject"]
        mail_send(message=message, subject=subject)
        messages.add_message(request, messages.INFO, "Report sent")
        return render(request, "report_view.html", context)
    elif context["pdf"]:
        filename = "%s-%s-%s.pdf" % (context["company_name"], "report", pk)
        return render_pdf(context, filename=filename, template="report.html")
    else:
        return render(request, "report_view.html", context)


@staff_member_required
def report_edit(request, pk=None):
    """
    """

    return edit(
        request,
        report_model=Report,
        form_model=ReportForm,
        model=Report,
        invoice_model=Invoice,
        pk=pk,
        project_model=Project,
    )


@staff_member_required
def report_index(request):
    """
    """

    context = get_index_items(
        model=Report,
        order_by=("-date",),
        request=request,
        search_fields=("id", "name", "gross", "net"),
    )
    return render(request, "report_index.html", context)


@staff_member_required
def service_edit(request, pk=None):
    """
    """

    return edit(request, form_model=ServiceForm, model=Service, pk=pk)


@staff_member_required
def service_index(request):
    """
    """

    context = get_index_items(
        model=Service,
        report_model=Report,
        order_by=("-active", "name"),
        request=request,
        search_fields=("name",),
    )
    return render(request, "service_index.html", context)


@staff_member_required
def service_view(request, pk=None):
    """
    """

    context = get_page_items(model=Service, pk=pk, request=request, report_model=Report)
    return render(request, "service_view.html", context)


@staff_member_required
def task_view(request, pk=None):
    """
    """

    context = get_page_items(
        model=Task,
        pk=pk,
        request=request,
        report_model=Report,
        include_fields=("name", "rate"),
    )
    return render(request, "task_view.html", context)


@staff_member_required
def task_edit(request, pk=None):
    """
    """

    return edit(request, form_model=TaskForm, model=Task, pk=pk)


@staff_member_required
def task_index(request):
    """
    """

    context = get_index_items(
        model=Task,
        report_model=Report,
        order_by=("-active", "name"),
        request=request,
        search_fields=("name",),
    )
    return render(request, "task_index.html", context)


@login_required
def time_view(request, pk=None):
    """
    Authenticated users can only view their own time entries unless
    they are staff.
    """

    time = get_object_or_404(Time, pk=pk)
    if not request.user.is_staff and not time.user:  # No user
        messages.add_message(request, messages.WARNING, FOUR_O_3)
        return HttpResponseRedirect(reverse("home"))
    elif (
        not request.user.is_staff and not time.user.username == request.user.username
    ):  # Time entry user does not match user
        messages.add_message(request, messages.WARNING, FOUR_O_3)
        return HttpResponseRedirect(reverse("home"))
    else:
        context = get_page_items(
            model=Time,
            pk=pk,
            request=request,
            report_model=Report,
            include_fields=("date", "project", "hours", "description"),
        )
        return render(request, "time_view.html", context)


@login_required
def time_edit(request, pk=None):
    """
    Authenticated users can only edit their own time entries unless
    they are staff.
    """

    if pk is not None:
        time = get_object_or_404(Time, pk=pk)
        if not request.user.is_staff and not time.user:  # No user
            messages.add_message(request, messages.WARNING, FOUR_O_3)
            return HttpResponseRedirect(reverse("home"))
        elif (
            not request.user.is_staff
            and not time.user.username == request.user.username
        ):  # Time entry user does not match user
            messages.add_message(request, messages.WARNING, FOUR_O_3)
            return HttpResponseRedirect(reverse("home"))
    if request.user.is_staff:
        time_form = AdminTimeForm
    else:
        time_form = TimeForm
    return edit(
        request,
        form_model=time_form,
        model=Time,
        invoice_model=Invoice,
        estimate_model=Estimate,
        project_model=Project,
        report_model=Report,
        task_model=Task,
        time_model=Time,
        pk=pk,
    )


@staff_member_required
def time_index(request):
    """
    """

    search_fields = (
        "client__name",
        "date",
        "description",
        "pk",
        "project__name",
        "hours",
        "invoice__pk",
        "user__username",
        "task__name",
    )
    context = get_index_items(
        model=Time,
        report_model=Report,
        filter_by={"time": {"estimate": None, "user__isnull": False}},
        order_by=("-date",),
        request=request,
        search_fields=search_fields,
    )
    return render(request, "time_index.html", context)


@login_required
def user_view(request, pk=None):
    """
    """

    if not request.user.pk == int(pk) and not request.user.is_staff:
        messages.add_message(request, messages.WARNING, FOUR_O_3)
        return HttpResponseRedirect(reverse("home"))
    else:
        order_by = {"time": ("-updated",), "project": ("-updated",)}
        context = get_page_items(
            contact_model=Contact,
            model=User,
            order_by=order_by,
            profile_model=Profile,
            project_model=Project,
            include_fields=(
                "rate",
                "bio",
                "address",
                "job_title",
                "twitter_username",
                "notifications",
            ),
            report_model=Report,
            time_model=Time,
            pk=pk,
            request=request,
        )
        return render(request, "user_view.html", context)


@login_required
def user_edit(request, pk=None):
    """
    """

    if pk is not None:
        if has_profile(request.user):
            if not request.user.pk == int(pk) and not request.user.is_staff:
                messages.add_message(request, messages.WARNING, FOUR_O_3)
                return HttpResponseRedirect(reverse("home"))
    if request.user.is_staff:
        profile_form = AdminProfileForm
    else:
        profile_form = ProfileForm
    return edit(
        request, form_model=profile_form, model=User, pk=pk, profile_model=Profile
    )


@staff_member_required
def user_index(request):
    """
    """

    context = get_index_items(
        report_model=Report,
        model=User,
        order_by=("-profile__active", "last_name", "first_name"),
        request=request,
        search_fields=("first_name", "last_name", "id", "email", "username"),
    )
    return render(request, "user_index.html", context)
