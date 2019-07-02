from django.db.models import F
from django.db.models import Sum
from decimal import Decimal


def get_total(field, **kwargs):
    """
    Calculate and return net, gross, cost amounts based on field. No object storage here.
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
    """
    estimate = kwargs.get("estimate")
    invoice = kwargs.get("invoice")
    project = kwargs.get("project")
    invoice_amount = 0
    entry_amount = 0
    project_cost = 0
    hours = 0
    for time_entry in times:
        hours = time_entry.hours
        if time_entry.task:
            rate = time_entry.task.rate
            if rate:
                entry_amount = rate * hours  # Currency
        time_entry.amount = "%.2f" % entry_amount
        invoice_amount += entry_amount
    if invoice:
        invoice.amount = "%.2f" % invoice_amount
        invoice.save()
    elif estimate:
        estimate.amount = "%.2f" % invoice_amount
        estimate.save()
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
        project.amount = "%.2f" % invoice_amount
        project.cost = "%.2f" % project_cost
        project.hours = hours
        project.save()
    return times
