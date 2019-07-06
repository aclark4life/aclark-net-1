from hashlib import md5


def has_profile(user):
    return hasattr(user, "profile")


def gravatar_url(email):
    """
    MD5 hash of email address for use with Gravatar. Return generic
    if none exists.
    """
    try:
        return gravatar_url % md5(email.lower()).hexdigest()
    except AttributeError:
        # https://stackoverflow.com/a/7585378/185820
        return gravatar_url % md5("db@aclark.net".encode("utf-8")).hexdigest()


def set_items(model_name, items=None, _items={}):
    """
    Share templates by returning dictionary of items e.g.
        for item in items.reports
    instead of:
        for item in reports
    """
    i = {}
    i["%ss" % model_name] = items

    for key in _items.keys():
        i[key] = _items[key]

    return i


def get_setting(request, setting, settings_model=None, page_size=None):
    """
    Return setting from user profile model or system config
    """

    if not request.user.is_authenticated:
        return

    if setting == "page_size":
        if has_profile(request.user):
            return request.user.profile.page_size
