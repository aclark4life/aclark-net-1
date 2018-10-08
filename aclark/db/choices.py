# https://github.com/goinnn/django-multiselectfield
COLOR_CHOICES = (
    ('primary', 'Primary'),
    ('secondary', 'Secondary'),
    ('success', 'Success'),
    ('danger', 'Danger'),
    ('warning', 'Warning'),
    ('info', 'Info'),
    ('light', 'Light'),
    ('dark', 'Dark'),
    ('muted', 'Muted'),
    ('white', 'White'),
)

DASHBOARD_ITEMS = (
    ('times', 'Times'),
    ('totals', 'Totals'),
)

EDITOR_CHOICES = (
    ('ckeditor', 'CKEditor'),
    ('tinymce', 'TinyMCE'),
)

ICON_CHOICES = (
    ('1x', 'Small'),
    ('2x', 'Medium'),
    ('3x', 'Large'),
    ('4x', 'XL'),
    ('5x', 'XXL'),
)

TEMPLATE_CHOICES = (
    ('mail_html.html', 'Mail'),
    ('cerberus-fluid.html', 'Fluid'),
    ('cerberus-hybrid.html', 'Hybrid'),
    ('cerberus-responsive.html', 'Responsive'),
)

PAYMENT_CHOICES = (
    ('', '---'),
    ('check', 'Check'),
    ('paypal', 'PayPal'),
    ('wire', 'Wire'),
)

ESTIMATE_TYPES = (
    ('', '---'),
    ('is_sow', 'Statement of Work'),
    ('is_to', 'Task Order'),
)

# Not really a choice, but close enough.

URL_NAMES = {
    'Settings App': ('settings_app', 'settings_app_edit', ''),
    'Settings Company': ('company_view', 'company_edit', ''),
    'Settings Contract': ('settings_contract', 'settings_contract_edit', ''),
    'client': ('client_view', 'client_edit', 'client_index'),
    'contact': ('contact_view', 'contact_edit', 'contact_index'),
    'contract': ('contract_view', 'contract_edit', 'contract_index'),
    'estimate': ('estimate_view', 'estimate_edit', 'estimate_index'),
    'file': ('file_view', 'file_edit', 'file_index'),
    'invoice': ('invoice_view', 'invoice_edit', 'invoice_index'),
    'log': ('log_view', 'log_edit', 'log_index'),
    'newsletter': ('newsletter_view', 'newsletter_edit', 'newsletter_index'),
    'note': ('note_view', 'note_edit', 'note_index'),
    'profile': ('user_view', 'user_edit', 'user_index'),
    'project': ('project_view', 'project_edit', 'project_index'),
    'proposal': ('proposal_view', 'proposal_edit', 'proposal_index'),
    'report': ('report_view', 'report_edit', 'report_index'),
    'service': ('', 'service_edit', ''),
    'task': ('task_view', 'task_edit', 'task_index'),
    'time': ('time_view', 'time_edit', 'time_index'),
    'user': ('user_view', 'user_edit', 'user_index'),
}
