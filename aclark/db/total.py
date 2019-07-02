from django.db.models import F
from django.db.models import Sum
from decimal import Decimal


def get_total(field, **kwargs):
    """
    Given a field & queryset, calculate & return net, gross, cost; no object storage.
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
    Given a queryset, calculate and store invoice, time & hours sums and project cost.
    """
    invoice = kwargs.get("invoice")
    project = kwargs.get("project")

    t_sum = 0
    invoice_sum = 0
    # Calculate sum for each time (t.amount) and all times (invoice_sum).
    for t in times:
        hours = t.hours
        if t.task:
            rate = t.task.rate
            if rate:
                t_sum = rate * hours
        t.amount = "%.2f" % t_sum
        invoice_sum += t_sum

    # If invoice, save invoice sum to invoice.
    cost = 0
    if invoice:
        invoice.amount = "%.2f" % invoice_sum
        invoice.save()
    # If project, save invoice total (gross) & project cost to project.
    elif project:
        users = project.team.all()
        if users:
            for user in users:
                times = times.filter(user=user)
                hours = get_total("hours", times=times)
                rate = user.profile.rate
                if hours:
                    hours = Decimal(hours)
                    if rate:
                        cost += rate * hours
        project.cost = "%.2f" % cost
        project.hours = hours
        project.amount = "%.2f" % invoice_sum
        project.save()
    return times
