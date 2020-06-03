from django.core.mail import send_mail


def get_recipients(obj):
    """
    Given obj, return obj's recipients.
    """

    if not obj:
        return []
    model_name = obj._meta.verbose_name
    if model_name == "contact":
        return [(obj.first_name, obj.email)]
    elif model_name == "estimate":
        return [(i.first_name, i.email) for i in obj.contacts.all()]
    elif model_name == "note":
        return [(i.first_name, i.email) for i in obj.contacts.all()]
    elif model_name == "project":
        return [
            (i.first_name, i.email, i.profile.notifications) for i in obj.team.all()
        ]
    elif model_name == "time":
        return [("Alex", "aclark@aclark.net")]


def mail_send(**kwargs):
    """
    Send mail with Django
    """

    mail_from = kwargs.get("mail_from", "aclark@aclark.net")
    mail_to = kwargs.get("mail_to", "aclark@aclark.net")
    html_message = kwargs.get("html_message")
    message = kwargs.get("message", "Test")
    subject = kwargs.get("subject", "Test")
    if html_message:
        send_mail(
            subject,
            message,
            mail_from,
            (mail_to,),
            fail_silently=False,
            html_message=html_message,
        )
    else:
        send_mail(subject, message, mail_from, (mail_to,), fail_silently=False)
