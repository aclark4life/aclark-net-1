from django.db.models import Q
from operator import or_ as OR
from functools import reduce
from .misc import set_items


def get_search_results(
    context,
    model,
    search_fields,
    search,
    edit_url=None,
    view_url=None,
    order_by=None,
    request=None,
):
    """
    """

    query = []
    model_name = model._meta.verbose_name
    for field in search_fields:
        query.append(Q(**{field + "__icontains": search}))
    items = model.objects.filter(reduce(OR, query))
    context["%s_nav" % model_name] = True
    context["edit_url"] = edit_url
    context["view_url"] = view_url
    if order_by is not None:
        items = items.order_by(*order_by)
    items = set_items(model_name, items=items)
    context["items"] = items
    return context
