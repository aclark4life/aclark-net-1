from django.db.models import F
from django.db.models import Sum
from decimal import Decimal


def get_total(field, **kwargs):
    """
    Given a field & queryset, calculate & return net, gross, cost; no object storage.
    """

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
    Given a queryset, calculate and store invoice, time & hours totals and project cost.
    """
    invoice = kwargs.get("invoice")
    project = kwargs.get("project")

    hours = 0
    cost = 0
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
    if invoice:
        invoice.amount = "%.2f" % invoice_sum
        invoice.save()

    # If project, save invoice sum to project.
    elif project:
        # team = project.team.all()
        # if team:
        #     hours = get_total(field="hours", times=times, team=team)
        #     if "users" in hours:
        #         for user in hours["users"]:
        #             rate = user.profile.rate
        #             user_hours = Decimal(hours["users"][user])
        #             user.hours = user_hours
        #            user.save()
        #            if rate:
        #                project_cost += rate * user_hours
        # project.cost = "%.2f" % project_cost
        # project.hours = hours
        project.amount = "%.2f" % invoice_sum
        project.save()
    return times
