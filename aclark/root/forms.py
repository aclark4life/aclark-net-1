from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class ContactForm(forms.Form):
    first_name = forms.CharField(
        label="First Name"
    )
    last_name = forms.CharField(
        label="Last Name"
    )
    email = forms.CharField(
        label="Email", widget=forms.EmailInput(attrs={"class": "email"})
    )
    message = forms.CharField(
        label="How can we help you?", widget=forms.Textarea(attrs={"class": "message"})
    )
    captcha = ReCaptchaField(label="Protected by reCAPTCHA v3", widget=ReCaptchaV3)
