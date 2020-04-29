from django.conf.urls import url
from django.conf.urls import include
from . import views

urlpatterns = [
    url(r"^$", views.home, name="dashboard"),
    url(r"^auth/", include("django.contrib.auth.urls")),
    # Account
    url(r"^account/(?P<pk>\d+)$", views.account_view, name="account_view"),
    url(r"^account/(?P<pk>\d+)/edit$", views.account_edit, name="account_edit"),
    url(r"^account/add$", views.account_edit, name="account_edit"),
    url(r"^account$", views.account_index, name="account_index"),
    # Client
    url(r"^client/(?P<pk>\d+)$", views.client_view, name="client_view"),
    url(r"^client/(?P<pk>\d+)/edit$", views.client_edit, name="client_edit"),
    url(r"^client/add$", views.client_edit, name="client_edit"),
    url(r"^client$", views.client_index, name="client_index"),
    # Competency
    url(r"^competency$", views.competency, name="competency"),
    # Contact
    url(r"^contact/(?P<pk>\d+)$", views.contact_view, name="contact_view"),
    url(r"^contact/(?P<pk>\d+)/edit$", views.contact_edit, name="contact_edit"),
    url(r"^contact/add$", views.contact_edit, name="contact_edit"),
    url(r"^contact$", views.contact_index, name="contact_index"),
    # Error (forced)
    url(r"^500$", views.error, name="error"),
    # Estimate
    url(r"^estimate/(?P<pk>\d+)$", views.estimate_view, name="estimate_view"),
    url(r"^estimate/(?P<pk>\d+)/edit$", views.estimate_edit, name="estimate_edit"),
    url(r"^estimate/add$", views.estimate_edit, name="estimate_edit"),
    url(r"^estimate$", views.estimate_index, name="estimate_index"),
    # Invoice
    url(r"^invoice/(?P<pk>\d+)$", views.invoice_view, name="invoice_view"),
    url(r"^invoice/(?P<pk>\d+)/edit$", views.invoice_edit, name="invoice_edit"),
    url(r"^invoice/add$", views.invoice_edit, name="invoice_edit"),
    url(r"^invoice$", views.invoice_index, name="invoice_index"),
    # Login
    url(r"^login$", views.login, name="login"),
    url(r"^logout$", views.logout, name="logout"),
    # Note
    url(r"^note/(?P<pk>\d+)$", views.note_view, name="note_view"),
    url(r"^note/(?P<pk>\d+)/edit$", views.note_edit, name="note_edit"),
    url(r"^note/add$", views.note_edit, name="note_edit"),
    url(r"^note$", views.note_index, name="note_index"),
    # Order
    url(r"^order/(?P<pk>\d+)$", views.order_view, name="order_view"),
    url(r"^order/(?P<pk>\d+)/edit$", views.order_edit, name="order_edit"),
    url(r"^order/add$", views.order_edit, name="order_edit"),
    url(r"^order$", views.order_index, name="order_index"),
    # Project
    url(r"^project/(?P<pk>\d+)$", views.project_view, name="project_view"),
    url(r"^project/(?P<pk>\d+)/edit$", views.project_edit, name="project_edit"),
    url(r"^project/add$", views.project_edit, name="project_edit"),
    url(r"^project$", views.project_index, name="project_index"),
    # Report
    url(r"^report/(?P<pk>\d+)$", views.report_view, name="report_view"),
    url(r"^report$", views.report_index, name="report_index"),
    url(r"^report/add$", views.report_edit, name="report_edit"),
    url(r"^report/(?P<pk>\d+)/edit$", views.report_edit, name="report_edit"),
    # Service
    url(r"^service/(?P<pk>\d+)$", views.service_view, name="service_view"),
    url(r"^service$", views.service_index, name="service_index"),
    url(r"^service/add$", views.service_edit, name="service_edit"),
    url(r"^service/(?P<pk>\d+)/edit$", views.service_edit, name="service_edit"),
    # Social
    url("", include("social_django.urls", namespace="social")),
    # Task
    url(r"^task/(?P<pk>\d+)$", views.task_view, name="task_view"),
    url(r"^task/(?P<pk>\d+)/edit$", views.task_edit, name="task_edit"),
    url(r"^task/add$", views.task_edit, name="task_edit"),
    url(r"^task$", views.task_index, name="task_index"),
    # Task Orders
    url(r"^taskorder/(?P<pk>\d+)$", views.task_order_view, name="task_order_view"),
    url(r"^taskorder/(?P<pk>\d+)/edit$", views.task_order_edit, name="task_order_edit"),
    url(r"^taskorder/add$", views.task_order_edit, name="task_order_edit"),
    url(r"^taskorder$", views.task_order_index, name="task_order_index"),
    # Time
    url(r"^time/(?P<pk>\d+)$", views.time_view, name="time_view"),
    url(r"^time/(?P<pk>\d+)/edit$", views.time_edit, name="time_edit"),
    url(r"^time/add$", views.time_edit, name="time_edit"),
    url(r"^time$", views.time_index, name="time_index"),
    # User
    url(r"^user/(?P<pk>\d+)$", views.user_view, name="user_view"),
    url(r"^user/(?P<pk>\d+)/edit$", views.user_edit, name="user_edit"),
    url(r"^user/add$", views.user_edit, name="user_edit"),
    url(r"^user$", views.user_index, name="user_index"),
]
