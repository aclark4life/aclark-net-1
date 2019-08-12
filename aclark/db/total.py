from django.db.models import F
from django.db.models import Sum


def get_total(field, **kwargs):
    """
    Given a field & queryset, calculate & return net, gross, cost sums; no object storage.
    """

    # querysets
    invoices = kwargs.get("invoices")
    projects = kwargs.get("projects")
    times = kwargs.get("times")

    if field == "gross" and invoices:
        gross = invoices.aggregate(amount=Sum(F("amount")))["amount"]
        if gross is None:
            return 0
        else:
            return gross
    elif field == "cost" and projects:
        cost = projects.aggregate(cost=Sum(F("cost")))["cost"]
        if gross is None:
            return 0
        else:
            return cost
    elif field == "hours" and times:
        hours = times.aggregate(hours=Sum(F("hours")))["hours"]
        return hours


def set_total(times, **kwargs):
    """
    """
    project = kwargs.get("project")
    invoice = kwargs.get("invoice")
    time_model = kwargs.get("time_model")

    # Calculate & save invoice & time amounts
    amount = 0
    invoice_amount = 0
    for t in times:
        if t.task:
            if t.task.rate:
                amount = t.task.rate * t.hours
        t.amount = "%.2f" % amount
        t.save()
        invoice_amount += amount

    if invoice:
        invoice.amount = "%.2f" % invoice_amount
        invoice.save()

    elif project:
        project.amount = "%.2f" % invoice_amount
        cost = 0
        users = project.team.all()
        for user in users:
            times = time_model.objects.filter(
                estimate=None, invoiced=False, user=user, project=project
            )
            hours = get_total("hours", times=times)
            if user.profile.rate and hours:
                cost += user.profile.rate * hours
        project.cost = cost
        project.save()
    return times
