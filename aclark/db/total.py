from django.db.models import F
from django.db.models import Sum
from decimal import Decimal


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
        return gross
    elif field == "cost" and projects:
        cost = projects.aggregate(cost=Sum(F("cost")))["cost"]
        return cost
    elif field == "hours" and times:
        hours = times.aggregate(hours=Sum(F("hours")))["hours"]
        return hours


def set_total(times, **kwargs):
    """
    """
    project = kwargs.get("project")
    invoice = kwargs.get("invoice")

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
        cost = 0
        hours = 0
        users = project.team.all()
        project.user_hours = {}
        if users:
            for user in users:
                times = times.filter(user=user)
                hours = get_total("hours", times=times)
                if hours:
                    project.user_hours[user.username] = str(hours)
                    hours = Decimal(hours)
                    if user.profile.rate:
                        cost += user.profile.rate * hours
        project.amount = "%.2f" % invoice_amount
        project.cost = "%.2f" % cost
        project.hours = hours
        project.save()
    return times
