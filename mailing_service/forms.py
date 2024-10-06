from django import forms
from .models import MailingRecipient, MailingMessage


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['email', 'full_name', 'comment']


class MailingMessageForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = ['subject', 'body']
