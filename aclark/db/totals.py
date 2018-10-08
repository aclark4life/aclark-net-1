from django.db.models import F
from django.db.models import Sum
from decimal import Decimal


def get_total(**kwargs):
    """
    Given object or field, return total currency or time
    """
    field = kwargs.get('field')
    invoices = kwargs.get('invoices')
    projects = kwargs.get('projects')
    times = kwargs.get('times')
    team = kwargs.get('team')
    total = {}
    if field == 'amount' and invoices:  # Currency
        amount = invoices.aggregate(amount=Sum(F('amount')))['amount']
        total['amount'] = amount
    elif field == 'cost' and projects:  # Currency
        cost = projects.aggregate(cost=Sum(F('cost')))['cost']
        total['cost'] = cost
    elif field == 'hours' and times:  # Time
        total['hours'] = 0
        total_hours = times.aggregate(hours=Sum(F('hours')))['hours']
        if total_hours:
            total['hours'] = total_hours
        if team:
            total['users'] = {}
            for user in team:
                total['users'][user] = 0
                times_user = times.filter(user=user)
                hours_user = times_user.aggregate(
                    hours=Sum(F('hours')))['hours']
                if hours_user:
                    total['users'][user] = hours_user
    else:
        total['cost'] = 0
        total['hours'] = 0
        total['amount'] = 0
    return total


def set_total(times, **kwargs):
    """
    Given times and object, set total currency on object
    """
    estimate = kwargs.get('estimate')
    invoice = kwargs.get('invoice')
    project = kwargs.get('project')
    invoice_amount = 0
    time_amount = 0
    for time_entry in times:
        hours = time_entry.hours
        if time_entry.task:
            rate = time_entry.task.rate
            if rate:
                time_amount = rate * hours  # Currency
        time_entry.amount = '%.2f' % time_amount
        invoice_amount += time_amount
    if invoice:
        invoice.amount = '%.2f' % invoice_amount
        invoice.save()
    elif estimate:
        estimate.amount = '%.2f' % invoice_amount
        estimate.save()
    elif project:
        cost = 0
        team = project.team.all()
        if team:
            hours = get_total(field='hours', times=times, team=team)
            if 'users' in hours:
                for user in hours['users']:
                    rate = user.profile.rate
                    if rate:
                        cost += rate * Decimal(hours['users'][user])
        project.amount = '%.2f' % invoice_amount
        project.cost = '%.2f' % cost
        project.save()
    return times
