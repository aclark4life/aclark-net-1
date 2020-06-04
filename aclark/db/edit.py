from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .form import get_form
from .mail import mail_send
from .misc import set_items
from .obj import obj_process
from .obj import set_ref
from .query import get_query_string


def edit(request, **kwargs):
    """
    """

    context = {}
    obj = None
    account_model = kwargs.get("account_model")
    client_model = kwargs.get("client_model")
    contact_model = kwargs.get("contact_model")
    estimate_model = kwargs.get("estimate_model")
    form_model = kwargs.get("form_model")
    invoice_model = kwargs.get("invoice_model")
    model = kwargs.get("model")
    note_model = kwargs.get("note_model")
    pk = kwargs.get("pk")
    project_model = kwargs.get("project_model")
    report_model = kwargs.get("report_model")
    user_model = kwargs.get("user_model")
    task_order_model = kwargs.get("task_order_model")
    model_name = None
    new_time = False

    if model:
        model_name = model._meta.verbose_name
        context["%s_nav" % model_name] = True

    if pk is None:  # New obj
        form = get_form(
            account_model=account_model,
            client_model=client_model,
            form_model=form_model,
            invoice_model=invoice_model,
            task_order_model=task_order_model,
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

    if contact_model:
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
                obj, query_checkbox=query_checkbox, request=request, task="check"
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
                account_model=account_model,
                client_model=client_model,
                estimate_model=estimate_model,
                invoice_model=invoice_model,
                task_order_model=task_order_model,
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

    if model_name == "account":
        context["account_nav"] = True
    elif model_name == "client":
        context["client_nav"] = True
    elif model_name == "contact":
        context["contact_nav"] = True
    elif model_name == "estimate":
        context["estimate_nav"] = True
    elif model_name == "invoice":
        context["invoice_nav"] = True
    elif model_name == "note":
        context["note_nav"] = True
    elif model_name == "project":
        context["project_nav"] = True
    elif model_name == "task":
        context["task_nav"] = True
    elif model_name == "time":
        context["time_nav"] = True
    elif model_name == "user":
        context["user_nav"] = True

    items = {}
    if report_model:
        reports = report_model.objects.filter(active=True).order_by("-date")
        items = set_items("report", items=reports)
    context["items"] = items

    return render(request, template_name, context)
