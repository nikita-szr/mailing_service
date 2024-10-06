from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import MailingRecipient


class MailingRecepientListView(ListView):
    model = MailingRecipient
    template_name = 'mailing_service/recepient_list.html'
    context_object_name = "recepients"


class MailingRecepientDetailView(DetailView):
    model = MailingRecipient
    template_name = 'mailing_service/recepient_detail.html'
    context_object_name = "recepient"


class MailingRecepientCreateView(CreateView):
    model = MailingRecipient
    template_name = 'mailing_service/recepient_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('mailing_service:recepient_list')


class MailingRecepintUpdateView(UpdateView):
    model = MailingRecipient
    template_name = 'mailing_service/recepient_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('mailing_service:recepient_list')


class MailingRecepientDeleteView(DeleteView):
    model = MailingRecipient
    template_name = 'mailing_service/recepient_confirm_delete.html'
    success_url = reverse_lazy('mailing_service:recepient_list')

