from collections import OrderedDict


def get_fields(item, include=[]):
    _fields = item._meta._get_fields()
    fields = OrderedDict()
    for field in _fields:
        if field.name in include:
            value = getattr(item, field.name)
            fields[field.name] = value
    return fields
