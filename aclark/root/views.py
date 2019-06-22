from .forms import ContactForm
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
import os
import random
import requests
from aclark.db.models import Client

# Create your views here.

BASE_URL = "https://%s" % os.environ.get("API_HOST", "aclark.net")
SERVICE_URL = "%s/api/services/?format=json" % BASE_URL
TESTIMONIAL_URL = "%s/api/testimonials/?format=json" % BASE_URL
PROFILE_URL = "%s/api/profiles/?format=json" % BASE_URL

EMAIL_FROM = "aclark@aclark.net"


def about(request):
    context = {}
    testimonials = requests.get(TESTIMONIAL_URL).json()
    context["testimonial"] = random.choice(testimonials)
    context["about_nav"] = True
    return render(request, "about.html", context)


def blog(request):
    return HttpResponseRedirect("http://blog.aclark.net")


def clients(request):
    context = {}
    clients_government = Client.objects.filter(tags__name__in=["government",], published=True)
    clients_non_profit = Client.objects.filter(tags__name__in=["non-profit",], published=True)
    clients_private_sector = Client.objects.filter(tags__name__in=["private-sector",], published=True)
    clients_colleges_universities = Client.objects.filter(tags__name__in=["colleges-universities",], published=True)
    context['clients_government'] = clients_government
    context['clients_non_profit'] = clients_non_profit
    context['clients_private_sector'] = clients_private_sector
    context['clients_colleges_universities'] = clients_colleges_universities
    context['clients_nav'] = True
    return render(request, "clients.html", context)


def contact(request):
    context = {}
    now = timezone.datetime.now
    msg = "Message sent!"
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["email"]
            message = "\n\n".join([message, sender])
            recipients = [EMAIL_FROM]
            subject = "Contact %s" % now().strftime("%m/%d/%Y %H:%M")
            send_mail(subject, message, EMAIL_FROM, recipients)
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(reverse("home"))
    else:
        form = ContactForm()
    context["form"] = form
    return render(request, "contact.html", context)


def home(request):
    context = {}
    testimonials = requests.get(TESTIMONIAL_URL).json()
    context["testimonial"] = random.choice(testimonials)
    context['home_nav'] = True
    return render(request, "base.html", context)


def services(request):
    context = {}
    services = requests.get(SERVICE_URL).json()
    context["services"] = services
    context['services_nav'] = True
    return render(request, "services.html", context)


def testimonials(request):
    context = {}
    testimonials = requests.get(TESTIMONIAL_URL).json()
    context["testimonials"] = testimonials
    return render(request, "testimonials.html", context)


def team(request):
    context = {}
    profiles = requests.get(PROFILE_URL).json()
    context["profiles"] = profiles
    context["about_nav"] = True
    return render(request, "team.html", context)
