# https://github.com/goinnn/django-multiselectfield
COLOR_CHOICES = (
    ("primary", "Primary"),
    ("secondary", "Secondary"),
    ("success", "Success"),
    ("danger", "Danger"),
    ("warning", "Warning"),
    ("info", "Info"),
    ("light", "Light"),
    ("dark", "Dark"),
    ("muted", "Muted"),
    ("white", "White"),
)

DASHBOARD_ITEMS = (("tools", "Tools"), ("times", "Times"), ("totals",
                                                            "Totals"))

EDITOR_CHOICES = (("ckeditor", "CKEditor"), ("tinymce", "TinyMCE"))

ICON_CHOICES = (
    ("1x", "Small"),
    ("2x", "Medium"),
    ("3x", "Large"),
    ("4x", "XL"),
    ("5x", "XXL"),
)

PAYMENT_CHOICES = (
    ("", "---"),
    ("check", "Check"),
    ("paypal", "PayPal"),
    ("wire", "Wire"),
)

# Not really a choice, but close enough.

URL_NAMES = {
    "Settings App": ("app_view", "app_edit", ""),
    "Settings Company": ("company_view", "company_edit", ""),
    "client": ("client_view", "client_edit", "client_index"),
    "contact": ("contact_view", "contact_edit", "contact_index"),
    "estimate": ("estimate_view", "estimate_edit", "estimate_index"),
    "invoice": ("invoice_view", "invoice_edit", "invoice_index"),
    "note": ("note_view", "note_edit", "note_index"),
    "profile": ("user_view", "user_edit", "user_index"),
    "project": ("project_view", "project_edit", "project_index"),
    "report": ("report_view", "report_edit", "report_index"),
    "task": ("task_view", "task_edit", "task_index"),
    "time": ("time_view", "time_edit", "time_index"),
    "user": ("user_view", "user_edit", "user_index"),
    "order": ("order_view", "order_edit", "order_index"),
}
