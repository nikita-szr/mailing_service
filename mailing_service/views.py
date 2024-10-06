from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import MailingRecipient, MailingMessage, Mailing
from .forms import MailingRecipientForm, MailingMessageForm, MailingForm


class MailingRecipientListView(ListView):
    model = MailingRecipient
    template_name = 'mailing_service/recipient_list.html'
    context_object_name = "recipients"


class MailingRecipientDetailView(DetailView):
    model = MailingRecipient
    template_name = 'mailing_service/recipient_detail.html'
    context_object_name = "recipient"


class MailingRecipientCreateView(CreateView):
    model = MailingRecipient
    template_name = 'mailing_service/recipient_form.html'
    form = MailingRecipientForm
    success_url = reverse_lazy('mailing_service:recipient_list')


class MailingRecipientUpdateView(UpdateView):
    model = MailingRecipient
    template_name = 'mailing_service/recipient_form.html'
    form = MailingRecipientForm
    success_url = reverse_lazy('mailing_service:recipient_list')


class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    template_name = 'mailing_service/recipient_confirm_delete.html'
    context_object_name = 'recipient'
    success_url = reverse_lazy('mailing_service:recipient_list')


class MailingMessageListView(ListView):
    model = MailingMessage
    template_name = 'mailing_service/message_list.html'
    context_object_name = "messages"


class MailingMessageDetailView(DetailView):
    model = MailingMessage
    template_name = 'mailing_service/message_detail.html'
    context_object_name = "message"


class MailingMessageCreateView(CreateView):
    model = MailingMessage
    template_name = 'mailing_service/message_form.html'
    form = MailingMessageForm
    success_url = reverse_lazy('mailing_service:message_list')


class MailingMessageUpdateView(UpdateView):
    model = MailingMessage
    template_name = 'mailing_service/message_form.html'
    form = MailingMessageForm
    success_url = reverse_lazy('mailing_service:message_list')


class MailingMessageDeleteView(DeleteView):
    model = MailingMessage
    template_name = 'mailing_service/message_confirm_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mailing_service:message_list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_service/mailing_list.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing_service/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing_service/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_service:mailing_list')
