from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.decorators.cache import cache_control, cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import (MailingForm, MailingMessageForm, MailingRecipientForm,
                    UserRegistrationForm)
from .models import (CustomUser, Mailing, MailingAttempt, MailingMessage,
                     MailingRecipient)


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingRecipientListView(LoginRequiredMixin, ListView):
    model = MailingRecipient
    template_name = 'mailing_service/recipient_list.html'
    context_object_name = "recipients"

    def get_queryset(self):
        if self.request.user.is_staff:
            return MailingRecipient.objects.all()
        return MailingRecipient.objects.filter(user=self.request.user)


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingRecipientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MailingRecipient
    template_name = 'mailing_service/recipient_detail.html'
    context_object_name = "recipient"

    def test_func(self):
        recipient = self.get_object()
        return self.request.user.is_staff or recipient.user == self.request.user


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    template_name = 'mailing_service/recipient_form.html'
    form_class = MailingRecipientForm
    success_url = reverse_lazy('mailing_service:recipient_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingRecipientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingRecipient
    template_name = 'mailing_service/recipient_form.html'
    form_class = MailingRecipientForm
    success_url = reverse_lazy('mailing_service:recipient_list')

    def test_func(self):
        recipient = self.get_object()
        return recipient.user == self.request.user


class MailingRecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingRecipient
    template_name = 'mailing_service/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing_service:recipient_list')

    def test_func(self):
        recipient = self.get_object()
        return recipient.user == self.request.user


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingMessageListView(ListView):
    model = MailingMessage
    template_name = 'mailing_service/message_list.html'
    context_object_name = "messages"


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingMessageDetailView(DetailView):
    model = MailingMessage
    template_name = 'mailing_service/message_detail.html'
    context_object_name = "message"


class MailingMessageCreateView(CreateView):
    model = MailingMessage
    template_name = 'mailing_service/message_form.html'
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing_service:message_list')


class MailingMessageUpdateView(UpdateView):
    model = MailingMessage
    template_name = 'mailing_service/message_form.html'
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing_service:message_list')


class MailingMessageDeleteView(DeleteView):
    model = MailingMessage
    template_name = 'mailing_service/message_confirm_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mailing_service:message_list')


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_service/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=self.request.user)


@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = 'mailing_service/mailing_detail.html'
    context_object_name = 'mailing'

    def test_func(self):
        mailing = self.get_object()
        return self.request.user.is_staff or mailing.user == self.request.user


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


class MailingSendView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        if self.test_func():
            mailing.send()
        return redirect('mailing_service:mailing_detail', pk=pk)

    def test_func(self):
        mailing = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        return self.request.user.is_staff or mailing.user == self.request.user


@method_decorator(cache_control(public=True, max_age=86400), name='dispatch')
class HomePageView(TemplateView):
    template_name = 'mailing_service/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_mailings'] = Mailing.objects.count()

        context['active_mailings'] = Mailing.objects.filter(status='started').count()

        context['unique_recipients'] = MailingRecipient.objects.values('email').distinct().count()

        return context


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'mailing_service/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            subject = "Подтверждение регистрации"
            message = "Перейдите по ссылке для подтверждения регистрации: " \
                      f"{request.build_absolute_uri(reverse('mailing_service:confirm_email',
                                                            args=[urlsafe_base64_encode(force_bytes(user.pk)),
                                                                  default_token_generator.make_token(user)]))}"
            send_mail(subject, message, 'admin@example.com', [user.email])
            return redirect('mailing_service:registration_complete')
        return render(request, 'mailing_service/register.html', {'form': form})


class ConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            return render(request, 'mailing_service/confirm_email.html')
        else:
            return HttpResponse('Ссылка для подтверждения недействительна.')


@login_required
def statistics_view(request):
    user = request.user

    mailings = Mailing.objects.filter(recipients__email=user.email)

    total_attempts = MailingAttempt.objects.filter(mailing__in=mailings).count()
    successful_attempts = MailingAttempt.objects.filter(mailing__in=mailings, status='success').count()
    failed_attempts = MailingAttempt.objects.filter(mailing__in=mailings, status='failure').count()
    total_sent_messages = sum(mailing.recipients.count() for mailing in mailings)

    context = {
        'total_attempts': total_attempts,
        'successful_attempts': successful_attempts,
        'failed_attempts': failed_attempts,
        'total_sent_messages': total_sent_messages,
    }

    return render(request, 'statistics.html', context)
