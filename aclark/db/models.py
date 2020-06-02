from .utils import gravatar_url
from django.conf import settings

# from django.contrib.gis.db import models
from django.db import models
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager
from uuid import uuid4

# https://github.com/lazybird/django-solo
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default="Site Name")
    maintenance_mode = models.BooleanField(default=False)

    company = models.ForeignKey(
        "Company",
        blank=True,
        null=True,
        limit_choices_to={"active": True},
        on_delete=models.CASCADE,
    )

    company_name = models.CharField(max_length=255, default="Company Name")
    company_address = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"


class BaseModel(models.Model):
    """
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)
    tags = TaggableManager(blank=True, help_text="")

    class Meta:
        abstract = True


class Client(BaseModel):
    """
    """

    published = models.BooleanField(default=False)
    name = models.CharField(max_length=300, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField("Website", blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["name"]


class Contact(BaseModel):
    """
    Client, First Name, Last Name, Title, Email, Office Phone, Mobile Phone,
    Fax
    """

    subscribed = models.BooleanField(default=True)
    client = models.ForeignKey(
        Client,
        blank=True,
        null=True,
        limit_choices_to={"active": True},
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField("E-Mail Address", blank=True, null=True)
    mobile_phone = PhoneNumberField("Mobile Phone", blank=True, null=True)
    office_phone = PhoneNumberField("Office Phone", blank=True, null=True)
    fax = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    uuid = models.UUIDField("UUID", max_length=300, default=uuid4)

    def __str__(self):
        if self.email and self.first_name and self.last_name:
            return " ".join([self.first_name, self.last_name, "<%s>" % self.email])
        elif self.first_name and self.last_name:
            return " ".join([self.first_name, self.last_name])
        elif self.first_name:
            return " ".join([self.first_name])
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])


class Company(BaseModel):
    """
    """

    published = models.BooleanField(default=False)
    name = models.CharField(max_length=300, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField("Website", blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"


class Estimate(BaseModel):
    """
    Issue Date, Estimate ID, Client, Subject, Estimate Amount, Subtotal,
    Discount, Tax, Tax2, Currency, Accepted Date, Declined Date
    """

    subject = models.CharField(max_length=300, blank=True, null=True)
    issue_date = models.DateField(
        "Issue Date", blank=True, null=True, default=timezone.now
    )
    client = models.ForeignKey(
        Client,
        blank=True,
        null=True,
        limit_choices_to={"active": True},
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        "Estimate Amount", blank=True, null=True, max_digits=12, decimal_places=2
    )
    discount = models.IntegerField(blank=True, null=True)
    tax = models.IntegerField(blank=True, null=True)
    tax2 = models.IntegerField(blank=True, null=True)
    currency = models.CharField(
        max_length=300, blank=True, default="United States Dollar - USD", null=True
    )
    accepted_date = models.DateField(blank=True, null=True)
    declined_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(
        "Start Date", blank=True, default=timezone.now, null=True
    )
    end_date = models.DateField("End Date", blank=True, default=timezone.now, null=True)
    project = models.ForeignKey(
        "Project",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    contacts = models.ManyToManyField("Contact", blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"profile__active": True},
    )
    task = models.ForeignKey(
        "Task",
        blank=True,
        null=True,
        limit_choices_to={"active": True},
        on_delete=models.CASCADE,
    )
    note = models.ManyToManyField("Note", blank=True, limit_choices_to={"active": True})

    def __str__(self):
        return "estimate-%s" % self.pk


class Invoice(BaseModel):
    """
    Issue Date, Last Payment Date, Invoice ID, PO Number, Client, Subject,
    Invoice Amount, Paid Amount, Balance, Subtotal, Discount, Tax, Tax2,
    Currency, Currency Symbol
    """

    subject = models.CharField(max_length=300, blank=True, null=True)
    issue_date = models.DateField(
        "Issue Date", blank=True, default=timezone.now, null=True
    )
    due_date = models.DateField("Due", blank=True, null=True)
    last_payment_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(
        "Start Date", blank=True, default=timezone.now, null=True
    )
    end_date = models.DateField("End Date", blank=True, default=timezone.now, null=True)
    po_number = models.CharField("PO Number", max_length=300, blank=True, null=True)
    sa_number = models.CharField(
        "Subcontractor Agreement Number", max_length=300, blank=True, null=True
    )
    client = models.ForeignKey(
        Client,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    amount = models.DecimalField(
        "Invoice Amount", blank=True, null=True, max_digits=12, decimal_places=2
    )
    paid_amount = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    balance = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    subtotal = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    discount = models.IntegerField(blank=True, null=True)
    tax = models.IntegerField(blank=True, null=True)
    tax2 = models.IntegerField(blank=True, null=True)
    project = models.ForeignKey(
        "Project",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    currency = models.CharField(
        default="United States Dollar - USD", max_length=300, blank=True, null=True
    )
    currency_symbol = models.CharField(
        default="$", max_length=300, blank=True, null=True
    )
    note = models.ManyToManyField("Note", blank=True, limit_choices_to={"active": True})

    def __str__(self):
        if self.subject:
            return self.subject
        else:
            return "invoice-%s" % self.pk

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["subject"]

    doc_type = models.CharField(max_length=300, blank=True, null=True)


class Order(BaseModel):
    """
    """

    date_arrived = models.DateField("Due", blank=True, null=True)
    date_expected = models.DateField("Due", blank=True, null=True)
    date_shipped = models.DateField("Due", blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])


class Note(BaseModel):
    """
    """

    due_date = models.DateField("Due", blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])


class Profile(BaseModel):
    """
    """

    published = models.BooleanField(default=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    page_size = models.PositiveIntegerField(blank=True, null=True)
    rate = models.DecimalField(
        "Hourly Rate (United States Dollar - USD)",
        blank=True,
        null=True,
        max_digits=12,
        decimal_places=2,
    )
    unit = models.DecimalField(
        "Unit", default=1.0, blank=True, null=True, max_digits=12, decimal_places=2
    )
    avatar_url = models.URLField("Avatar URL", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    job_title = models.CharField(max_length=150, blank=True, null=True)
    twitter_username = models.CharField(max_length=150, blank=True, null=True)
    notifications = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    def get_avatar_url(self):
        if self.avatar_url is not None:
            return self.avatar_url
        else:
            return gravatar_url(self.user.email)

    def get_username(self):
        if self.preferred_username is not None:
            return self.preferred_username
        elif self.user:
            return self.user.username
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    def is_staff(self):
        if self.user:
            if self.user.is_staff:
                return True


class Project(BaseModel):
    """
    Client, Project, Project Code, Start Date, End Date,
    Total Hours, Billable Hours, Billable Amount, Budget, Budget Spent,
    Budget Remaining, Total Costs, Team Costs, Expenses
    """

    client = models.ForeignKey(
        Client,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    name = models.CharField("Project Name", max_length=300, blank=True, null=True)
    task = models.ForeignKey(
        "Task",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    team = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, limit_choices_to={"profile__active": True}
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    code = models.IntegerField("Project Code", blank=True, null=True)
    total_hours = models.FloatField(blank=True, null=True)
    billable_hours = models.FloatField(blank=True, null=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    budget = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    budget_spent = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    budget_remaining = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    total_costs = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    team_costs = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    cost = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    expenses = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["name"]


class Report(BaseModel):
    """
    """

    name = models.CharField(max_length=300, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    cost = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    gross = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    net = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    invoices = models.ManyToManyField("Invoice", blank=True)

    def __str__(self):
        return "report-%s" % self.date


class Service(BaseModel):
    """
    """

    published = models.BooleanField(default=False)
    name = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["name"]


class Testimonial(BaseModel):
    """
    """

    name = models.CharField(max_length=300, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    issue_date = models.DateField(
        "Issue Date", blank=True, null=True, default=timezone.now
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])


class Task(BaseModel):
    """
    """

    billable = models.BooleanField(default=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    rate = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2)
    unit = models.DecimalField(
        "Unit", default=1.0, blank=True, null=True, max_digits=12, decimal_places=2
    )

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://stackoverflow.com/a/6062320/185820
    class Meta:
        ordering = ["name"]


class Time(BaseModel):
    """
    Date, Client, Project, Project Code, Task, Hours, Billable?,
    Invoiced?, First Name, Last Name, Department, Employee?, Billable
    Rate, Billable Amount, Cost Rate, Cost Amount, Currency,
    External Reference URL
    """

    billable = models.BooleanField(default=True)
    employee = models.BooleanField(default=True)
    invoiced = models.BooleanField(default=False)
    client = models.ForeignKey(
        Client,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    project = models.ForeignKey(
        Project,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    task = models.ForeignKey(
        Task,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={"active": True},
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"profile__active": True},
    )
    estimate = models.ForeignKey(
        Estimate, blank=True, null=True, on_delete=models.SET_NULL
    )
    invoice = models.ForeignKey(
        Invoice,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"last_payment_date": None},
    )
    date = models.DateField(default=timezone.now)
    hours = models.DecimalField(
        "Hours", default=1.0, blank=True, null=True, max_digits=12, decimal_places=2
    )
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    department = models.CharField(max_length=300, blank=True, null=True)
    cost_rate = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    cost_amount = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    currency = models.CharField(max_length=300, blank=True, null=True)
    external_reference_url = models.URLField(blank=True, null=True)
    project_code = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "-".join([self._meta.verbose_name, str(self.pk)])

    # https://docs.djangoproject.com/en/1.9/ref/models/instances/#get-absolute-url
    def get_absolute_url(self, hostname):
        return "%s/%s" % (hostname, reverse("time_view", args=[str(self.id)]))


class Account(BaseModel):
    """
    """

    name = models.CharField(max_length=300, blank=True, null=True)
    number = models.CharField(max_length=300, blank=True, null=True)
    url = models.URLField(max_length=300, blank=True, null=True)
    note = models.ManyToManyField("Note", blank=True, limit_choices_to={"active": True})

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "-".join([self._meta.verbose_name, str(self.pk)])
