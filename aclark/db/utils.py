from django.db.models import F
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .fields import get_fields
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

    model_name = model._meta.verbose_name
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

    if report_model:
        reports = report_model.objects.filter(active=True).order_by("-date")

    context = {}

    items = set_items(model_name, items=items)

    if not request.user.is_authenticated:  # Don't show anon
        items = []

    context["items"] = items

    context["edit_url"] = edit_url
    context["view_url"] = view_url

    context["page"] = page_num
    context["paginated"] = paginated

    context["%s_nav" % model_name] = True

    # Return search index items
    if request.method == "POST":
        if search == u"":  # Empty search returns none
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

    contact_model = kwargs.get("contact_model")
    estimate_model = kwargs.get("estimate_model")
    invoice_model = kwargs.get("invoice_model")
    note_model = kwargs.get("note_model")
    project_model = kwargs.get("project_model")
    report_model = kwargs.get("report_model")
    time_model = kwargs.get("time_model")

    model = kwargs.get("model")
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

    net = 0
    gross = 0
    hours = 0
    cost = 0

    context = {}
    item = None
    items = None
    model_name = None
    fields = None
    config = None

    last_payment_date = None

    if model:
        model_name = model._meta.verbose_name
        if model_name == "client":
            item = get_object_or_404(model, pk=pk)
            contacts = contact_model.objects.filter(client=item)
            estimates = estimate_model.objects.filter(client=item)
            invoices = invoice_model.objects.filter(client=item)
            projects = project_model.objects.filter(client=item)
            notes = note_model.objects.filter(client=item)
            if order_by:
                invoices = invoices.order_by(*order_by["invoice"])
                projects = projects.order_by(*order_by["project"])
                contacts = contacts.order_by(*order_by["contact"])
            items = set_items("contact", items=contacts)
            items = set_items("invoice", items=invoices, _items=items)
            items = set_items("note", items=notes, _items=items)
            items = set_items("project", items=projects, _items=items)
            items = set_items("estimate", items=estimates, _items=items)
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
            config = (
                site_config_model.get_solo()
            )  # get_solo will create the item if it does not already exist
        elif model_name == "invoice":
            item = get_object_or_404(model, pk=pk)
            config = (
                site_config_model.get_solo()
            )  # get_solo will create the item if it does not already exist
            times = time_model.objects.filter(estimate=None, invoice=item)
            times = times.order_by(*order_by["time"])
            times = set_total(times, invoice=item)
            last_payment_date = item.last_payment_date
        elif model_name == "project":
            item = get_object_or_404(model, pk=pk)
            contacts = contact_model.objects.all()
            estimates = estimate_model.objects.filter(project=item)
            invoices = invoice_model.objects.filter(project=item)
            notes = note_model.objects.filter(project=item)
            times = time_model.objects.filter(
                estimate=None, project=item, task__isnull=False, invoiced=False
            )
            times = set_total(times, project=item, time_model=time_model)
            if order_by:
                times = times.order_by(*order_by["time"])
                invoices = invoices.order_by(*order_by["invoice"])
            items = set_items("contact", items=contacts)
            items = set_items("estimate", items=estimates, _items=items)
            items = set_items("invoice", items=invoices, _items=items)
            items = set_items("time", items=times, _items=items)
            items = set_items("note", items=notes, _items=items)
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
        elif model_name == "task":
            item = get_object_or_404(model, pk=pk)
        elif model_name == "time":
            item = get_object_or_404(model, pk=pk)
            fields = get_fields(
                item, include_fields=include_fields
            )  # fields_table.html
        elif model_name == "user":
            item = get_object_or_404(model, pk=pk)
            projects = project_model.objects.filter(team__in=[item], active=True)
            projects = projects.order_by(*order_by["project"])
            times = time_model.objects.filter(estimate=None, invoiced=False, user=item)
            times = times.order_by(*order_by["time"])
            contacts = contact_model.objects.all()
            fields = get_fields(
                item.profile, include_fields=include_fields
            )  # fields_table.html
            hours = get_total("hours", times=times)
        elif model_name == "note":
            item = get_object_or_404(model, pk=pk)
            fields = get_fields(
                item, include_fields=include_fields
            )  # fields_items.html
        else:
            item = get_object_or_404(model, pk=pk)
            items = set_items(model_name, items=items)
    else:  # no model
        model_name = "home"
        # Items
        invoices = invoice_model.objects.filter(last_payment_date=None)
        invoices = invoices.order_by(*order_by["invoice"])
        projects = project_model.objects.filter(active=True, hidden=False)
        projects = projects.order_by(*order_by["project"])
        if filter_by:
            times = time_model.objects.filter(**filter_by["time"])
        else:
            times = time_model.objects.all()
        times = times.order_by(*order_by["time"])
        times = set_total(times)
        items = set_items("invoice", items=invoices)
        items = set_items("project", items=projects, _items=items)
        items = set_items("time", items=times, _items=items)
        # Paginate items
        page_num = get_query_string(request, "page")
        paginated = get_query_string(request, "paginated")
        if paginated:  # Paginate if paginated
            page_size = get_setting(request, "page_size")
            if "times" in items:
                items["times"] = paginate(
                    items["times"], page_num=page_num, page_size=page_size
                )
        # Totals

        gross = get_total("gross", invoices=invoices)
        hours = get_total("hours", times=times)
        cost = get_total("cost", projects=projects)
        if gross and cost:
            net = gross - cost

    if report_model:
        reports = report_model.objects.filter(active=True).order_by("-date")
        if items:
            items = set_items("report", items=reports, _items=items)
        else:
            items = set_items("report", items=reports)

    context["item"] = item
    context["net"] = net
    context["gross"] = gross
    context["hours"] = hours
    context["cost"] = cost
    context["items"] = items
    context["model_name"] = model_name
    context["%s_nav" % model_name] = True
    context["edit_url"] = "%s_edit" % model_name
    context["view_url"] = "%s_view" % model_name
    context["doc"] = doc
    context["mail"] = mail
    context["pdf"] = pdf
    context["request"] = request  # Include request
    context["fields"] = fields
    context["config"] = config
    context["last_payment_date"] = last_payment_date

    return context
