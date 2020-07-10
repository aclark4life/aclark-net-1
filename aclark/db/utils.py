from django.db.models import F
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from .fields import get_fields
from .mortgage import get_loan
from .misc import set_items
from .misc import get_setting
from .page import paginate
from .query import get_query_string
from .search import get_search_results
from .total import get_total
from .total import set_total

gravatar_url = "https://www.gravatar.com/avatar/%s"


def get_index_items(**kwargs):
    """
    """
    request = kwargs.get("request")
    model = kwargs.get("model")
    report_model = kwargs.get("report_model")
    filter_by = kwargs.get("filter_by")
    order_by = kwargs.get("order_by")
    search_fields = kwargs.get("search_fields")
    page_size = kwargs.get("page_size")
    home_nav = kwargs.get("home_nav")

    model_name = model._meta.verbose_name
    model_name = model_name.replace(" ", "_")
    edit_url = "%s_edit" % model_name
    view_url = "%s_view" % model_name

    page_num = get_query_string(request, "page")
    paginated = get_query_string(request, "paginated")
    search = get_query_string(request, "search")

    items = model.objects.all()

    if filter_by:
        items = items.filter(**filter_by[model_name])

    if order_by is not None:  # http://stackoverflow.com/a/20257999/185820
        items = items.order_by(*order_by)

    if paginated:  # Paginate if paginated
        page_size = get_setting(request, "page_size")
        items = paginate(items, page_num=page_num, page_size=page_size)

    context = {}

    items = set_items(model_name, items=items)

    if report_model:
        reports = report_model.objects.filter(active=True).order_by("-date")
        items = set_items("report", items=reports, _items=items)

    if not request.user.is_authenticated:  # Don't show anon
        items = []

    context["items"] = items

    context["edit_url"] = edit_url
    context["view_url"] = view_url

    context["page"] = page_num
    context["paginated"] = paginated
    context["home_nav"] = home_nav

    context["%s_nav" % model_name] = True

    # Return search index items
    if request.method == "POST":
        if search == u"":
            items = []  # Empty search returns none
            context["items"] = items
            return context
        else:
            return get_search_results(
                context,
                model,
                search_fields,
                search,
                edit_url=edit_url,
                view_url=view_url,
                order_by=order_by,
                request=request,
            )

    return context


def get_page_items(**kwargs):
    """
    """

    # Page items
    model = kwargs.get("model")

    # Extra models for page
    contact_model = kwargs.get("contact_model")
    client_model = kwargs.get("client_model")
    estimate_model = kwargs.get("estimate_model")
    invoice_model = kwargs.get("invoice_model")
    project_model = kwargs.get("project_model")
    report_model = kwargs.get("report_model")
    time_model = kwargs.get("time_model")
    service_model = kwargs.get("service_model")

    pk = kwargs.get("pk")

    filter_by = kwargs.get("filter_by")
    order_by = kwargs.get("order_by")
    include_fields = kwargs.get("include_fields")

    page_size = kwargs.get("page_size")
    site_config_model = kwargs.get("site_config_model")

    request = kwargs.get("request")

    doc = get_query_string(request, "doc")
    mail = get_query_string(request, "mail")
    pdf = get_query_string(request, "pdf")
    xls = get_query_string(request, "xls")

    net = 0
    gross = 0
    hours_entered = 0
    hours_approved = 0
    cost = 0

    context = {}
    item = None
    items = None
    model_name = None
    fields = None

    last_payment_date = None

    invoices = None
    projects = None
    times = None

    doc_type = "Invoice"

    # Mortgage loan
    loan = {}

    company_name = "Company"
    site_config = None
    if site_config_model:
        site_config = site_config_model.get_solo()
    if site_config:
        if hasattr(site_config.company, "name"):
            company_name = site_config.company.name
            company_name = slugify(company_name)
    if model:
        model_name = model._meta.verbose_name
        model_name = model_name.replace(" ", "_")
        if model_name == "client":
            item = get_object_or_404(model, pk=pk)
            contacts = contact_model.objects.filter(client=item)
            estimates = estimate_model.objects.filter(client=item)
            invoices = invoice_model.objects.filter(client=item)
            projects = project_model.objects.filter(client=item)
            if order_by:
                invoices = invoices.order_by(*order_by["invoice"])
                projects = projects.order_by(*order_by["project"])
                contacts = contacts.order_by(*order_by["contact"])
            items = set_items("contact", items=contacts)
            items = set_items("invoice", items=invoices, _items=items)
            items = set_items("project", items=projects, _items=items)
            items = set_items("estimate", items=estimates, _items=items)
        elif model_name == "company":
            item = get_object_or_404(model, pk=pk)
            fields = get_fields(
                item, include_fields=include_fields
            )  # fields_items.html
        elif model_name == "contact":
            item = get_object_or_404(model, pk=pk)
            fields = get_fields(
                item, include_fields=include_fields
            )  # fields_items.html
        elif model_name == "estimate":  # handle obj or model
            item = get_object_or_404(model, pk=pk)
            times = time_model.objects.filter(estimate=item)
            if order_by:
                times = times.order_by(*order_by["time"])
            times = set_total(times, estimate=item)
            items = set_items("time", items=times)
        elif model_name == "invoice":
            item = get_object_or_404(model, pk=pk)
            times = time_model.objects.filter(estimate=None, invoice=item)
            if order_by:
                times = times.order_by(*order_by["time"])
            times = set_total(times, invoice=item)
            items = set_items("time", items=times)
            last_payment_date = item.last_payment_date
            doc_type = item.doc_type
        elif model_name == "task_order":
            item = get_object_or_404(model, pk=pk)
            times = time_model.objects.filter(task_order=item)
            if order_by:
                times = times.order_by(*order_by["time"])
            times = set_total(times, task_order=item)
            items = set_items("time", items=times)
        elif model_name == "project":
            item = get_object_or_404(model, pk=pk)
            contacts = contact_model.objects.all()
            estimates = estimate_model.objects.filter(project=item)
            invoices = invoice_model.objects.filter(project=item)
            times = time_model.objects.filter(
                estimate=None, project=item, task__isnull=False, invoiced=False
            )
            times = set_total(times, project=item, time_model=time_model)
            if order_by:
                times = times.order_by(*order_by["time"])
                invoices = invoices.order_by(*order_by["invoice"])
            users = item.team.all()
            items = set_items("contact", items=contacts)
            items = set_items("estimate", items=estimates, _items=items)
            items = set_items("invoice", items=invoices, _items=items)
            items = set_items("time", items=times, _items=items)
            items = set_items("user", items=users, _items=items)
        elif model_name == "report":
            item = get_object_or_404(model, pk=pk)
            reports = model.objects.filter(active=True).order_by("-date")
            reports.aggregate(cost=Sum(F("cost")))
            reports.aggregate(gross=Sum(F("gross")))
            reports.aggregate(net=Sum(F("net")))
            invoices = item.invoices.all()
            items = set_items("invoice", items=invoices)
            items = set_items("report", items=reports, _items=items)
            # E-Mail
            context["message"] = "Cost: %s, Gross: %s, Net: %s" % (
                item.cost,
                item.gross,
                item.net,
            )
            context["subject"] = item.name
        elif model_name == "service":
            item = get_object_or_404(model, pk=pk)
        elif model_name == "task":
            item = get_object_or_404(model, pk=pk)
            fields = get_fields(
                item, include_fields=include_fields
            )  # fields_items.html
        elif model_name == "time":
            item = get_object_or_404(model, pk=pk)
            fields = get_fields(
                item, include_fields=include_fields
            )  # fields_table.html
        elif model_name == "user":
            item = get_object_or_404(model, pk=pk)
            projects = project_model.objects.filter(team__in=[item], active=True)
            projects = projects.order_by(*order_by["project"])
            contacts = contact_model.objects.all()
            fields = get_fields(
                item.profile, include_fields=include_fields
            )  # fields_table.html
            # Hours entered
            times = time_model.objects.filter(estimate=None, invoiced=False, user=item)
            times = times.order_by(*order_by["time"])
            hours_entered = get_total("hours", times=times)
            # Hours approved
            times = times.filter(invoice__isnull=False)
            hours_approved = get_total("hours", times=times)
        elif model_name == "note":
            item = get_object_or_404(model, pk=pk)
            fields = get_fields(
                item, include_fields=include_fields
            )  # fields_items.html
            # E-Mail
            context["message"] = item.text
            context["subject"] = item.title
        else:
            item = get_object_or_404(model, pk=pk)
            items = set_items(model_name, items=items)
    else:  # no model
        model_name = "home"
        # Items
        if client_model:
            # Via aclark/root/views.py
            clients_government = client_model.objects.filter(
                tags__name__in=["government"], published=True
            )
            clients_non_profit = client_model.objects.filter(
                tags__name__in=["non-profit"], published=True
            )
            clients_private_sector = client_model.objects.filter(
                tags__name__in=["private-sector"], published=True
            )
            clients_colleges_universities = client_model.objects.filter(
                tags__name__in=["colleges-universities"], published=True
            )
            context["clients_government"] = clients_government
            context["clients_non_profit"] = clients_non_profit
            context["clients_private_sector"] = clients_private_sector
            context["clients_colleges_universities"] = clients_colleges_universities
        if invoice_model:
            invoices = invoice_model.objects.filter(last_payment_date=None)
            if order_by:
                invoices = invoices.order_by(*order_by["invoice"])
        if project_model:
            projects = project_model.objects.filter(active=True, hidden=False)
            if order_by:
                projects = projects.order_by(*order_by["project"])
        if service_model:
            services = service_model.objects.filter(active=True, hidden=False)
            context["services"] = services
        if time_model:
            times = time_model.objects.filter(**filter_by["time"])
            items = set_items("time", items=times)
        # Paginate items
        page_num = get_query_string(request, "page")
        paginated = get_query_string(request, "paginated")
        if paginated:  # Paginate if paginated
            page_size = get_setting(request, "page_size")
            if items:
                if "times" in items:
                    items["times"] = paginate(
                        items["times"], page_num=page_num, page_size=page_size
                    )
        # Totals
        gross = get_total("gross", invoices=invoices)
        cost = get_total("cost", projects=projects)
        net = gross - cost
        # Hours entered
        hours_entered = get_total("hours", times=times)
        # Hours approved
        times = times.filter(invoice__isnull=False)
        hours_approved = get_total("hours", times=times)
    if report_model:
        reports = report_model.objects.filter(active=True).order_by("-date")
        if items:
            items = set_items("report", items=reports, _items=items)
        else:
            items = set_items("report", items=reports)
    context["item"] = item
    context["net"] = net
    context["gross"] = gross
    context["hours_entered"] = hours_entered
    context["hours_approved"] = hours_approved
    context["cost"] = cost
    context["items"] = items
    context["model_name"] = model_name
    context["%s_nav" % model_name] = True
    context["edit_url"] = "%s_edit" % model_name
    context["view_url"] = "%s_view" % model_name
    context["doc"] = doc
    context["mail"] = mail
    context["pdf"] = pdf
    context["xls"] = xls
    context["request"] = request  # Include request
    context["fields"] = fields
    context["config"] = site_config
    context["last_payment_date"] = last_payment_date
    context["company_name"] = company_name
    context["doc_type"] = doc_type
    context["loan"] = loan

    return context
