from collections import OrderedDict


def get_fields(item, exclude_fields=[]):
    _fields = item._meta._get_fields()
    fields = OrderedDict()
    for field in _fields:
        if not field.is_relation and field.name not in exclude_fields:
            field_name = field.name.title().replace("_", " ")
            value = getattr(item, field.name)
            if value:
                try:
                    value = value.title()
                except AttributeError:  # Probably not "regular" field
                    pass
                fields[field_name] = value
    return fields
