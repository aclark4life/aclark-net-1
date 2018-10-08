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
    ('html_mail.html', 'Mail'),
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
