from django.db.models import F
from django.db.models import Sum


def get_total(field, **kwargs):
    """
    Given field & queryset calculate & return field sum
    """

    # queryset
    invoices = kwargs.get("invoices")
    projects = kwargs.get("projects")
    times = kwargs.get("times")
    # field
    gross = 0
    cost = 0
    hours = 0
    if field == "gross" and invoices:
        gross = invoices.aggregate(amount=Sum(F("amount")))["amount"]
        return gross
    elif field == "cost" and projects:
        cost = projects.aggregate(cost=Sum(F("cost")))["cost"]
        return cost
    elif field == "hours" and times:
        hours = times.aggregate(hours=Sum(F("hours")))["hours"]
        return hours
    return 0


def set_total(times, **kwargs):
    """
    """

    project = kwargs.get("project")
    estimate = kwargs.get("estimate")
    invoice = kwargs.get("invoice")
    time_model = kwargs.get("time_model")

    # Calculate & save invoice or estimate & time amounts
    amount = 0
    invoice_amount = 0
    estimate_amount = 0

    for t in times:
        if t.task:
            if t.task.rate:
                try:
                    amount = t.task.rate * t.hours
                except TypeError:
                    # Allow for None
                    pass
        t.amount = "%.2f" % amount
        t.save()
        if estimate:
            estimate_amount += amount
        elif invoice:
            invoice_amount += amount

    # Format
    if estimate:
        estimate.amount = "%.2f" % estimate_amount
        estimate.save()

    elif invoice:
        invoice.amount = "%.2f" % invoice_amount
        invoice.save()

    elif project:
        project.amount = "%.2f" % invoice_amount

        # Per user cost
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
