from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from . import choices


def obj_process(
    obj,
    app_settings_model=None,
    pk=None,
    request=None,
    task=None,
    model_name=None,
    page_type=None,
    query_checkbox=None,
    query_invoiced=None,
):
    """
    Process object based on task, typically performing some task followed by
    the appropriate redir.
    """
    http_ref = None
    if request:
        http_ref = request.META.get("HTTP_REFERER")
    if task == "url":
        if page_type == "view":
            url_name = choices.URL_NAMES[model_name][0]
            template_name = "%s.html" % url_name
            return template_name, url_name
        elif page_type == "copy":
            url_name = choices.URL_NAMES[model_name][1]
            return url_name
        elif page_type == "edit":
            template_name = "%s.html" % choices.URL_NAMES[model_name][1]
            return template_name
        elif page_type == "dashboard":
            url_name = "dashboard"
            return url_name
        elif page_type == "index":
            url_name = choices.URL_NAMES[model_name][2]
            return url_name
    elif task == "copy":
        dup = obj
        dup.pk = None
        dup.save()
        kwargs = {}
        kwargs["pk"] = dup.pk
        model_name = obj._meta.verbose_name
        url_name = obj_process(obj, model_name=model_name, page_type="copy", task="url")
        return HttpResponseRedirect(reverse(url_name, kwargs=kwargs))
    elif task == "redir":
        model_name = obj._meta.verbose_name
        template_name, url_name = obj_process(
            obj, model_name=model_name, page_type="view", task="url"
        )
        kwargs = {}
        if pk:  # Exists
            kwargs["pk"] = pk
            if model_name == "Settings App":  # Special cases for settings
                return HttpResponseRedirect(reverse(url_name))
            elif model_name == "Settings Company":
                return HttpResponseRedirect(reverse(url_name))
            elif model_name == "Settings Contract":
                return HttpResponseRedirect(reverse(url_name))
        else:  # New
            if model_name == "profile":  # One of to create profile for new
                kwargs["pk"] = obj.user.pk  # user
            else:
                kwargs["pk"] = obj.pk
        return HttpResponseRedirect(reverse(url_name, kwargs=kwargs))
    elif task == "remove":
        model_name = obj._meta.verbose_name
        if model_name == "time":  # Only admin can see index
            url_name = obj_process(
                obj, model_name=model_name, page_type="dashboard", task="url"
            )
        else:  # Admin can see index
            url_name = obj_process(
                obj, model_name=model_name, page_type="index", task="url"
            )
        if model_name == "profile":
            obj.user.delete()
        else:
            obj.delete()
        return HttpResponseRedirect(reverse(url_name))
    elif task == "invoiced":
        for time in obj.time_set.all():
            if query_invoiced["state"] == "true":
                time.invoiced = True
            elif query_invoiced["state"] == "false":
                time.invoiced = False
            time.save()
        if query_invoiced["state"] == "true":
            now = timezone.now()
            obj.last_payment_date = now
            messages.add_message(request, messages.INFO, "Sent!")
        elif query_invoiced["state"] == "false":
            messages.add_message(request, messages.INFO, "Not sent!")
            obj.last_payment_date = None
        obj.save()
        return HttpResponseRedirect(http_ref)
    elif task == "check":
        model_name = obj._meta.verbose_name
        if (
            query_checkbox["active"] == "on" or query_checkbox["active"] == "off"
        ):  # Active
            if query_checkbox["active"] == "on":
                obj.active = True
                obj.hidden = False
            else:
                obj.active = False
                if model_name == "note" and app_settings_model:
                    app_settings = app_settings_model.get_solo()
                    if app_settings.auto_hide:  # Auto-hide
                        obj.hidden = True
        elif (
            query_checkbox["subscribe"] == "on" or query_checkbox["subscribe"] == "off"
        ):  # Subscribe
            if query_checkbox["active"] == "on":
                obj.subscribed = True
            else:
                obj.subscribed = False
        obj.save()
        return HttpResponseRedirect(http_ref)
