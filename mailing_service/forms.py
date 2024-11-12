from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Mailing, MailingMessage, MailingRecipient


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['email', 'full_name', 'comment']


class MailingMessageForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = ['subject', 'body']


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_datetime', 'end_datetime', 'status', 'message', 'recipients']
        widgets = {
            'start_datetime': forms.DateTimeInput,
            'end_datetime': forms.DateTimeInput,
        }


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'avatar', 'phone_number', 'country')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)
