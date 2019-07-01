from django.db.models import Q
from django.db.models import F
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from faker import Faker
from functools import reduce
from operator import or_ as OR
from .fields import get_fields
from .form import get_form
from .mail import mail_send
from .misc import has_profile
from .obj import obj_process
from .page import paginate
from .query import get_query_string
from . import totals

fake = Faker()
gravatar_url = "https://www.gravatar.com/avatar/%s"


def edit(request, **kwargs):
    """
    """
    context = {}
    obj = None
    app_settings_model = kwargs.get("app_settings_model")
    contract_settings_model = kwargs.get("contract_settings_model")
    client_model = kwargs.get("client_model")
    company_model = kwargs.get("company_model")
    contact_model = kwargs.get("contact_model")
    estimate_model = kwargs.get("estimate_model")
    form_model = kwargs.get("form_model")
    invoice_model = kwargs.get("invoice_model")
    model = kwargs.get("model")
    note_model = kwargs.get("note_model")
    pk = kwargs.get("pk")
    project_model = kwargs.get("project_model")
    user_model = kwargs.get("user_model")
    model_name = None
    new_time = False

    if model:
        model_name = model._meta.verbose_name
        context["active_nav"] = model_name

    if pk is None:  # New obj
        form = get_form(
            client_model=client_model,
            contract_settings_model=contract_settings_model,
            form_model=form_model,
            invoice_model=invoice_model,
            model=model,
            project_model=project_model,
            user_model=user_model,
            request=request,
        )
    else:  # Existing obj
        obj = get_object_or_404(model, pk=pk)
        if model_name == "user":  # One-off to edit user profile
            obj = obj.profile
        form = get_form(
            form_model=form_model, obj=obj, project_model=project_model, request=request
        )

    if company_model:
        company = company_model.get_solo()
        company_name = company.name
        company_address = company.address
        currency_symbol = company.currency_symbol
        context["company_name"] = company_name
        context["company_address"] = company_address
        context["currency_symbol"] = currency_symbol
    elif contact_model:
        model_name = contact_model._meta.verbose_name
    elif note_model:
        model_name = note_model._meta.verbose_name

    if request.method == "POST":
        copy = get_query_string(request, "copy")
        delete = get_query_string(request, "delete")
        query_checkbox = get_query_string(request, "checkbox")
        query_invoiced = get_query_string(request, "invoiced")

        if pk is None:  # New obj
            form = form_model(request.POST)
            if model_name == "time":
                new_time = True
        else:  # Existing obj
            form = form_model(request.POST, instance=obj)

        if copy:
            return obj_process(obj, task="copy")

        if delete:
            return obj_process(obj, task="remove")

        if query_checkbox["condition"]:
            return obj_process(
                obj,
                query_checkbox=query_checkbox,
                app_settings_model=app_settings_model,
                request=request,
                task="check",
            )

        if query_invoiced["condition"]:
            return obj_process(
                obj, request=request, query_invoiced=query_invoiced, task="invoiced"
            )

        if form.is_valid():
            obj = form.save()
            if model_name == "time" and new_time:  # Send mail
                email_message = "%s/%s/edit" % ("https://aclark.net/db/time", obj.pk)
                email_subject = "Hey, looks like %s added time!" % request.user
                mail_send(message=email_message, subject=email_subject)
            set_ref(
                obj,
                request,
                client_model=client_model,
                company_model=company_model,
                estimate_model=estimate_model,
                invoice_model=invoice_model,
                model=model,
                project_model=project_model,
            )
            return obj_process(obj, pk=pk, task="redir")

    template_name = obj_process(
        obj, model_name=model_name, page_type="edit", task="url"
    )

    context["form"] = form
    context["item"] = obj
    context["pk"] = pk

    return render(request, template_name, context)


def generate_doc():
    """
    """

    # # https://stackoverflow.com/a/24122313/185820
    # document = Document()
    # # Head
    # task = ''
    # contract = context['item']
    # if contract.task:
    #     task = contract.task
    # title = document.add_heading(
    #     'ACLARK.NET, LLC %s AGREEMENT PREPARED FOR:' % task, level=1)
    # title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # if contract.client:
    #     client_name = document.add_heading(contract.client.name, level=1)
    #     client_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    #     client_address = document.add_heading(contract.client.address, level=1)
    #     client_address.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # parser = etree.HTMLParser()  # http://lxml.de/parsing.html
    # tree = etree.parse(StringIO(contract.body), parser)
    # # Body
    # for element in tree.iter():
    #     if element.tag == 'h2':
    #         document.add_heading(element.text, level=2)
    #     elif element.tag == 'p':
    #         document.add_paragraph(element.text)
    # response = HttpResponse(content_type=DOC)
    # response['Content-Disposition'] = 'attachment; filename=download.docx'
    # document.save(response)
    # return response

    # logo = kwargs.get('logo')
    # document.add_picture(logo, height=Inches(0.33))

    # p.add_run('bold').bold = True
    # p.add_run(' and some ')
    # p.add_run('italic.').italic = True

    # document.add_heading('Heading, level 1', level=1)
    # document.add_paragraph('Intense quote', style='Intense Quote')

    # document.add_paragraph(
    #     'first item in unordered list', style='List Bullet'
    # )
    # document.add_paragraph(
    #     'first item in ordered list', style='List Number'
    # )

    # records = (
    #     (3, '101', 'Spam'),
    #     (7, '422', 'Eggs'),
    #     (4, '631', 'Spam, spam, eggs, and spam')
    # )

    # table = document.add_table(rows=1, cols=3)
    # hdr_cells = table.rows[0].cells
    # hdr_cells[0].text = 'Qty'
    # hdr_cells[1].text = 'Id'
    # hdr_cells[2].text = 'Desc'
    # for qty, id, desc in records:
    #     row_cells = table.add_row().cells
    #     row_cells[0].text = str(qty)
    #     row_cells[1].text = id
    #     row_cells[2].text = desc
    # document.add_page_break()


def get_index_items(**kwargs):
    """
    """
    context = {}
    app_settings_model = kwargs.get("app_settings_model")
    company_model = kwargs.get("company_model")
    model = kwargs.get("model")
    filter_by = kwargs.get("filter_by")
    order_by = kwargs.get("order_by")
    page_size = kwargs.get("page_size")
    request = kwargs.get("request")
    search_fields = kwargs.get("search_fields")
    model_name = model._meta.verbose_name
    edit_url = "%s_edit" % model_name
    view_url = "%s_view" % model_name
    if company_model:
        company = company_model.get_solo()
        company_name = company.name
        company_address = company.address
        currency_symbol = company.currency_symbol
        context["company_name"] = company_name
        context["company_address"] = company_address
        context["currency_symbol"] = currency_symbol
    page_num = get_query_string(request, "page")
    paginated = get_query_string(request, "paginated")
    search = get_query_string(request, "search")
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
                app_settings_model=app_settings_model,
                edit_url=edit_url,
                view_url=view_url,
                order_by=order_by,
                request=request,
            )
    # Return filtered or all index items
    if filter_by:
        items = model.objects.filter(**filter_by[model_name])
    else:
        items = model.objects.all()
    if order_by is not None:  # Order items
        # http://stackoverflow.com/a/20257999/185820
        items = items.order_by(*order_by)
    if not request.user.is_authenticated:  # Don't show items to anon
        items = []
    if paginated:  # Paginate if paginated
        page_size = get_setting(request, "page_size")
        items = paginate(items, page_num=page_num, page_size=page_size)
    context["edit_url"] = edit_url
    context["view_url"] = view_url
    context["icon_size"] = get_setting(request, app_settings_model, "icon_size")
    context["icon_color"] = get_setting(request, app_settings_model, "icon_color")
    context["page"] = page_num
    context["paginated"] = paginated
    items = set_items(model_name, items=items)
    context["items"] = items
    context["active_nav"] = model_name
    return context


def get_page_items(**kwargs):
    app_settings_model = kwargs.get("app_settings_model")
    company_model = kwargs.get("company_model")
    contact_model = kwargs.get("contact_model")
    estimate_model = kwargs.get("estimate_model")
    contract_model = kwargs.get("contract_model")
    invoice_model = kwargs.get("invoice_model")
    note_model = kwargs.get("note_model")
    model = kwargs.get("model")
    obj = kwargs.get("obj")
    project_model = kwargs.get("project_model")
    request = kwargs.get("request")
    order_by = kwargs.get("order_by")
    pk = kwargs.get("pk")
    time_model = kwargs.get("time_model")
    user_model = kwargs.get("user_model")
    filter_by = kwargs.get("filter_by")
    page_size = kwargs.get("page_size")
    context = {}
    items = {}

    if request:  # Applies to all page items
        context["icon_color"] = get_setting(
            request, app_settings_model, "icon_color"
        )  # Prefs
        context["icon_size"] = get_setting(request, app_settings_model, "icon_size")
        doc = get_query_string(request, "doc")  # Export
        mail = get_query_string(request, "mail")  # Export
        pdf = get_query_string(request, "pdf")  # Export
        context["doc"] = doc
        context["mail"] = mail
        context["pdf"] = pdf
        context["request"] = request  # Include request

    if company_model:
        company = company_model.get_solo()
        company_name = company.name
        company_address = company.address
        currency_symbol = company.currency_symbol
        context["company_name"] = company_name
        context["company_address"] = company_address
        context["currency_symbol"] = currency_symbol

    model_name = None

    if model or obj:
        if model:
            model_name = model._meta.verbose_name
        elif obj:
            model_name = obj._meta.verbose_name

        context["model_name"] = model_name
        context["active_nav"] = model_name
        context["edit_url"] = "%s_edit" % model_name
        context["view_url"] = "%s_view" % model_name

        if model_name == "Settings App":
            app_settings = app_settings_model.get_solo()
            context["items"] = get_fields(app_settings)  # fields_items.html
        elif model_name == "Settings Company":
            company_settings = model.get_solo()
            context["item"] = get_fields(company_settings)  # fields_items.html
        elif model_name == "client":
            client = get_object_or_404(model, pk=pk)
            contacts = contact_model.objects.filter(client=client)
            contracts = contract_model.objects.filter(client=client)
            estimates = estimate_model.objects.filter(client=client)
            invoices = invoice_model.objects.filter(client=client)
            projects = project_model.objects.filter(client=client)
            notes = note_model.objects.filter(client=client)
            if order_by:
                invoices = invoices.order_by(*order_by["invoice"])
                projects = projects.order_by(*order_by["project"])
            items = set_items("contact", items=contacts)
            items = set_items("invoice", items=invoices, _items=items)
            items = set_items("note", items=notes, _items=items)
            items = set_items("project", items=projects, _items=items)
            items = set_items("estimate", items=estimates, _items=items)
            items = set_items("contract", items=contracts, _items=items)
            context["item"] = client
            context["items"] = items
        elif model_name == "contact":
            contact = get_object_or_404(model, pk=pk)
            context["items"] = get_fields(contact)  # fields_items.html
            context["item"] = contact
        elif model_name == "estimate":  # handle obj or model
            if not obj:
                estimate = get_object_or_404(model, pk=pk)
            else:
                estimate = obj
            times = time_model.objects.filter(estimate=estimate)
            if order_by:
                times = times.order_by(*order_by["time"])
            times = totals.set_total(times, estimate=estimate)
            context["doc_type"] = model_name
            context["entries"] = times
            context["item"] = estimate
        elif model_name == "order":  # handle obj or model
            if not obj:
                order = get_object_or_404(model, pk=pk)
            else:
                order = obj
            times = time_model.objects.filter(order=order)
            if order_by:
                times = times.order_by(*order_by["time"])
            times = totals.set_total(times, order=order)
            context["doc_type"] = "Statement of Work"
            context["entries"] = times
            context["item"] = order
        elif model_name == "invoice":
            invoice = get_object_or_404(model, pk=pk)
            times = time_model.objects.filter(estimate=None, invoice=invoice)
            times = times.order_by(*order_by["time"])
            times = totals.set_total(times, invoice=invoice)
            last_payment_date = invoice.last_payment_date
            context["doc_type"] = model_name
            context["entries"] = times
            context["item"] = invoice
            context["invoice"] = True
            context["last_payment_date"] = last_payment_date
        elif model_name == "project":
            project = get_object_or_404(model, pk=pk)
            context["item"] = project
            contacts = contact_model.objects.all()
            estimates = estimate_model.objects.filter(project=project)
            invoices = invoice_model.objects.filter(project=project)
            times = totals.set_total(
                time_model.objects.filter(
                    estimate=None, project=project, task__isnull=False, invoiced=False
                ),
                project=project,
            )
            if order_by:
                times = times.order_by(*order_by["time"])
                invoices = invoices.order_by(*order_by["invoice"])
            users = user_model.objects.filter(project=project)
            notes = note_model.objects.filter(project=project)
            items = set_items("contact", items=contacts)
            items = set_items("estimate", items=estimates, _items=items)
            items = set_items("invoice", items=invoices, _items=items)
            items = set_items("time", items=times, _items=items)
            items = set_items("user", items=users, _items=items)
            items = set_items("note", items=notes, _items=items)
            context["items"] = items
            context["cost"] = float(project.cost)
            context["gross"] = float(project.amount)
            context["net"] = float(project.amount) - float(project.cost)
        elif model_name == "report":
            report = get_object_or_404(model, pk=pk)
            reports = model.objects.filter(active=True)
            reports.aggregate(cost=Sum(F("cost")))
            reports.aggregate(gross=Sum(F("gross")))
            reports.aggregate(net=Sum(F("net")))
            invoices = report.invoices.all()
            items = set_items("invoice", items=invoices)
            context["item"] = report
            context["items"] = items
            context["reports"] = reports
            context["email_message"] = "Cost: %s, Gross: %s, Net: %s" % (
                report.cost,
                report.gross,
                report.net,
            )
            context["email_subject"] = report.name
        elif model_name == "task":
            task = get_object_or_404(model, pk=pk)
            context["item"] = task
        if model_name == "time":
            time = get_object_or_404(model, pk=pk)
            context["item"] = time
            fields = get_fields(time)  # fields_items.html
            context["fields"] = fields  # fields_items.html
        elif model_name == "user":
            user = get_object_or_404(model, pk=pk)
            projects = project_model.objects.filter(team__in=[user], active=True)
            projects = projects.order_by(*order_by["project"])
            times = time_model.objects.filter(estimate=None, invoiced=False, user=user)
            times = times.order_by(*order_by["time"])
            contacts = contact_model.objects.all()
            fields = get_fields(user.profile)  # fields_table.html
            context["fields"] = fields
            context["item"] = user
            context["projects"] = projects
            context["times"] = times
        else:
            item = get_object_or_404(model, pk=pk)
            context["item"] = item
    else:  # no model or obj
        if request:
            if request.user.is_authenticated:
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
                times = totals.set_total(times)
                items = set_items("invoice", items=invoices)
                items = set_items("project", items=projects, _items=items)
                items = set_items("time", items=times, _items=items)
                context["items"] = items
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
                total_amount = totals.get_total(field="amount", invoices=invoices)[
                    "amount"
                ]
                total_cost = totals.get_total(field="cost", projects=projects)["cost"]
                total_hours = totals.get_total(field="hours", times=times)["hours"]
                if total_amount and total_cost:
                    context["net"] = total_amount - total_cost
                context["cost"] = total_cost
                context["gross"] = total_amount
                context["hours"] = total_hours
                # Location
                ip_address = request.META.get("HTTP_X_REAL_IP")
                context["ip_address"] = ip_address
    return context


def get_search_results(
    context,
    model,
    search_fields,
    search,
    app_settings_model=None,
    edit_url=None,
    view_url=None,
    order_by=None,
    request=None,
):
    query = []
    model_name = model._meta.verbose_name
    for field in search_fields:
        query.append(Q(**{field + "__icontains": search}))
    items = model.objects.filter(reduce(OR, query))
    context["active_nav"] = model_name
    context["edit_url"] = edit_url
    context["view_url"] = view_url
    context["icon_size"] = get_setting(request, app_settings_model, "icon_size")
    context["icon_color"] = get_setting(request, app_settings_model, "icon_color")
    if order_by is not None:
        items = items.order_by(*order_by)
    items = set_items(model_name, items=items)
    context["items"] = items
    return context


def get_setting(request, setting, settings_model=None, page_size=None):
    """
    Return appropriate setting from user profile model or singleton settings
    model based on args
    """
    if not request.user.is_authenticated:
        return
    if setting == "icon_size":
        if has_profile(request.user):
            user_pref = request.user.profile.icon_size
        if user_pref:
            return user_pref
    elif setting == "icon_color":
        if has_profile(request.user):
            user_pref = request.user.profile.icon_color
        if user_pref:
            return user_pref
    elif setting == "page_size":
        if has_profile(request.user):
            user_pref = request.user.profile.page_size
        if user_pref:
            return user_pref
    elif setting == "dashboard_choices":
        if has_profile(request.user):
            user_pref = request.user.profile.dashboard_choices
        if user_pref:
            return user_pref
    elif setting == "exclude_hidden":
        app_settings = settings_model.get_solo()
        return app_settings.exclude_hidden


def set_items(model_name, items=None, _items={}):
    """
    Share templates by returning dictionary of items e.g.
        for item in items.reports
    instead of:
        for item in reports
    """
    _items["%ss" % model_name] = items
    return _items


def set_ref(obj, request, **kwargs):
    """
    Set object field references after create or edit
    """
    client_model = kwargs.get("client_model")
    company_model = kwargs.get("company_model")
    estimate_model = kwargs.get("estimate_model")
    invoice_model = kwargs.get("invoice_model")
    project_model = kwargs.get("project_model")
    model_name = obj._meta.verbose_name
    if model_name == "contact":
        query_client = get_query_string(request, "client")
        if query_client:
            client = get_object_or_404(client_model, pk=query_client)
            obj.client = client
            obj.save()
    elif model_name == "estimate" or model_name == "invoice":
        query_client = get_query_string(request, "client")
        query_project = get_query_string(request, "project")
        if query_project:
            project = get_object_or_404(project_model, pk=query_project)
            obj.client = project.client
            obj.project = project
            obj.save()
        if query_client:
            client = get_object_or_404(client_model, pk=query_client)
            obj.client = client
            obj.save()
    elif model_name == "note":
        query_client = get_query_string(request, "client")
        query_company = get_query_string(request, "company")
        query_invoice = get_query_string(request, "invoice")
        if query_client:
            client = get_object_or_404(client_model, pk=query_client)
            client.note.add(obj)
            client.save()
        elif query_company:
            company = company_model.get_solo()
            company.note.add(obj)
            company.save()
        elif query_invoice:
            invoice = get_object_or_404(invoice_model, pk=query_invoice)
            invoice.note.add(obj)
            invoice.save()
    elif model_name == "project":
        query_client = get_query_string(request, "client")
        if query_client:
            client = get_object_or_404(client_model, pk=query_client)
            obj.client = client
            obj.save()
    elif model_name == "contract":
        query_client = get_query_string(request, "client")
        if query_client:
            client = get_object_or_404(client_model, pk=query_client)
            obj.client = client
            obj.save()
    elif model_name == "time":
        if not obj.user:  # If no user, set user, else do nothing.
            obj.user = request.user
        query_estimate = get_query_string(request, "estimate")
        query_invoice = get_query_string(request, "invoice")
        query_project = get_query_string(request, "project")
        if query_estimate:
            estimate = get_object_or_404(estimate_model, pk=query_estimate)
            obj.estimate = estimate
        if query_invoice:
            invoice = get_object_or_404(invoice_model, pk=query_invoice)
            obj.invoice = invoice
            obj.save()  # Need save here to set more attrs
            obj.project = invoice.project
            obj.save()  # Need save here to set more attrs
            obj.task = invoice.project.task
        if query_project:
            project = get_object_or_404(project_model, pk=query_project)
            obj.project = project
            obj.save()  # Need save here to set more attrs
            if project.task:
                obj.task = project.task
        obj.save()
