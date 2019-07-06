from collections import OrderedDict


def get_fields(item, include_fields=[]):
    _fields = item._meta._get_fields()
    fields = OrderedDict()
    for field in _fields:
        if field.name in include_fields:
            value = getattr(item, field.name)
            fields[field.name] = value
    return fields
