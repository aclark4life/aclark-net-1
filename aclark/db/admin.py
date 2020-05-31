from decimal import Decimal
from django.contrib import admin
from import_export import fields
from import_export import widgets
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource as ImportExportModelResource
from .models import Account
from .models import Client
from .models import Company
from .models import Contact
from .models import Estimate
from .models import Invoice
from .models import Note
from .models import Order
from .models import Profile
from .models import Project
from .models import Report
from .models import StatementOfWork
from .models import Task
from .models import TaskOrder
from .models import Testimonial
from .models import Time


from solo.admin import SingletonModelAdmin
from aclark.db.models import SiteConfiguration

admin.site.register(SiteConfiguration, SingletonModelAdmin)


class BooleanWidget(widgets.Widget):
    """
    """

    def clean(self, value):
        """
        Return eval string value
        """
        if value == "Yes":
            return True
        else:
            return False


class DecimalWidget(widgets.Widget):
    """
    """

    def clean(self, value):
        """
        Return eval string value
        """
        if value:
            return Decimal(value.replace(",", ""))
        else:
            return Decimal(0)


class UserWidget(widgets.Widget):
    """
    """

    def clean(self, value):
        return value


# Register your models here.


class ClientResource(ImportExportModelResource):
    """
    """

    class Meta:
        model = Client

    # auto fill id? #295
    # https://github.com/django-import-export/django-import-export/issues/295
    def get_instance(self, instance_loaders, row):
        return False

    def before_import(self, dataset, dry_run, file_name=None, user=None):

        if dataset.headers:
            dataset.headers = [
                str(header).lower().strip() for header in dataset.headers
            ]

        if "id" not in dataset.headers:
            dataset.headers.append("id")


@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    """
    """

    resource_class = ClientResource


@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    """
    """


class ContactResource(ImportExportModelResource):
    """
    """

    client = fields.Field(
        column_name="client",
        attribute="client",
        widget=widgets.ForeignKeyWidget(Client, "name"),
    )

    class Meta:
        model = Contact

    def get_instance(self, instance_loaders, row):
        return False

    def before_import(self, dataset, dry_run, file_name=None, user=None):

        if dataset.headers:
            dataset.headers = [
                str(header).lower().strip() for header in dataset.headers
            ]

        if "id" not in dataset.headers:
            dataset.headers.append("id")


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    """
    """

    resource_class = ContactResource


class EstimateResource(ImportExportModelResource):
    """
    """

    client = fields.Field(
        column_name="client",
        attribute="client",
        widget=widgets.ForeignKeyWidget(Client, "name"),
    )
    amount = fields.Field(
        column_name="estimate_amount", attribute="amount", widget=DecimalWidget()
    )
    subtotal = fields.Field(
        column_name="subtotal", attribute="subtotal", widget=DecimalWidget()
    )
    document_id = fields.Field(
        column_name="estimate_id", attribute="document_id", widget=DecimalWidget()
    )

    class Meta:
        model = Estimate

    def get_instance(self, instance_loaders, row):
        return False

    def before_import(self, dataset, dry_run, file_name=None, user=None):

        if dataset.headers:
            dataset.headers = [
                str(header).lower().strip() for header in dataset.headers
            ]

        if "id" not in dataset.headers:
            dataset.headers.append("id")


@admin.register(Estimate)
class EstimateAdmin(ImportExportModelAdmin):
    """
    """

    resource_class = EstimateResource


class InvoiceResource(ImportExportModelResource):
    """
    """

    client = fields.Field(
        column_name="client",
        attribute="client",
        widget=widgets.ForeignKeyWidget(Client, "name"),
    )
    amount = fields.Field(
        column_name="amount", attribute="amount", widget=DecimalWidget()
    )
    paid_amount = fields.Field(
        column_name="paid_amount", attribute="paid_amount", widget=DecimalWidget()
    )
    subtotal = fields.Field(
        column_name="subtotal", attribute="subtotal", widget=DecimalWidget()
    )
    balance = fields.Field(
        column_name="balance", attribute="balance", widget=DecimalWidget()
    )
    document_id = fields.Field(
        column_name="invoice_id", attribute="document_id", widget=DecimalWidget()
    )

    class Meta:
        model = Invoice

    def get_instance(self, instance_loaders, row):
        return False

    def before_import(self, dataset, dry_run, file_name=None, user=None):

        if dataset.headers:
            dataset.headers = [
                str(header).lower().strip() for header in dataset.headers
            ]

        if "id" not in dataset.headers:
            dataset.headers.append("id")


@admin.register(Invoice)
class InvoiceAdmin(ImportExportModelAdmin):
    """
    """

    resource_class = InvoiceResource


@admin.register(Note)
class NoteAdmin(ImportExportModelAdmin):
    """
    """


@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    """
    """


class ProjectResource(ImportExportModelResource):
    """
    """

    client = fields.Field(
        column_name="client",
        attribute="client",
        widget=widgets.ForeignKeyWidget(Client, "name"),
    )
    billable_amount = fields.Field(
        column_name="billable_amount",
        attribute="billable_amount",
        widget=DecimalWidget(),
    )
    budget = fields.Field(
        column_name="budget", attribute="budget", widget=DecimalWidget()
    )
    budget_spent = fields.Field(
        column_name="budget_spent", attribute="budget_spent", widget=DecimalWidget()
    )
    team_costs = fields.Field(
        column_name="team_costs", attribute="team_costs", widget=DecimalWidget()
    )
    total_costs = fields.Field(
        column_name="total_costs", attribute="total_costs", widget=DecimalWidget()
    )

    class Meta:
        model = Project
        exclude = ("task", "team")

    def get_instance(self, instance_loaders, row):
        return False

    def before_import(self, dataset, dry_run, file_name=None, user=None):

        if dataset.headers:
            dataset.headers = [
                str(header).lower().strip() for header in dataset.headers
            ]

        if "id" not in dataset.headers:
            dataset.headers.append("id")


@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    """
    """


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    """
    """

    resource_class = ProjectResource


@admin.register(Report)
class ReportAdmin(ImportExportModelAdmin):
    """
    """


@admin.register(Testimonial)
class TestimonialAdmin(ImportExportModelAdmin):
    """
    """

    prepopulated_fields = {"slug": ("name",)}


class TaskResource(ImportExportModelResource):
    """
    """

    class Meta:
        model = Task
        exclude = ("unit", "billable", "active")

    def get_instance(self, instance_loaders, row):
        return False

    def before_import(self, dataset, dry_run, file_name=None, user=None):

        if dataset.headers:
            dataset.headers = [
                str(header).lower().strip() for header in dataset.headers
            ]

        if "id" not in dataset.headers:
            dataset.headers.append("id")


@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin):
    """
    """

    resource_class = TaskResource


class TimeResource(ImportExportModelResource):
    """
    """

    billable = fields.Field(
        column_name="billable", attribute="billable", widget=BooleanWidget()
    )
    client = fields.Field(
        column_name="client",
        attribute="client",
        widget=widgets.ForeignKeyWidget(Client, "name"),
    )
    invoiced = fields.Field(
        column_name="invoiced", attribute="invoiced", widget=BooleanWidget()
    )
    project = fields.Field(
        column_name="project",
        attribute="project",
        widget=widgets.ForeignKeyWidget(Project, "name"),
    )
    task = fields.Field(
        column_name="task",
        attribute="task",
        widget=widgets.ForeignKeyWidget(Task, "name"),
    )
    user = fields.Field(column_name="user", attribute="user", widget=UserWidget())

    class Meta:
        model = Time

    def get_instance(self, instance_loaders, row):
        return False

    def before_import(self, dataset, dry_run, file_name=None, user=None):

        if dataset.headers:
            dataset.headers = [
                str(header).lower().strip() for header in dataset.headers
            ]

        if "id" not in dataset.headers:
            dataset.headers.append("id")


@admin.register(Time)
class TimeAdmin(ImportExportModelAdmin):
    """
    """

    resource_class = TimeResource


@admin.register(StatementOfWork)
class StatementOfWorkAdmin(ImportExportModelAdmin):
    """
    """


@admin.register(TaskOrder)
class TaskOrderAdmin(ImportExportModelAdmin):
    """
    """


@admin.register(Account)
class TaskOrderAdmin(ImportExportModelAdmin):
    """
    """
