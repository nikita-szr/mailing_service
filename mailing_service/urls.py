from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (ConfirmEmailView, HomePageView, MailingCreateView,
                    MailingDeleteView, MailingDetailView, MailingListView,
                    MailingMessageCreateView, MailingMessageDeleteView,
                    MailingMessageDetailView, MailingMessageListView,
                    MailingMessageUpdateView, MailingRecipientCreateView,
                    MailingRecipientDeleteView, MailingRecipientDetailView,
                    MailingRecipientListView, MailingRecipientUpdateView,
                    MailingSendView, MailingUpdateView, RegisterView,
                    TemplateView, statistics_view, MailingAttemptListView)

app_name = 'mailing_service'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('recipient/recipients_list/', MailingRecipientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>/', MailingRecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/create/', MailingRecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/<int:pk>/update/', MailingRecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/<int:pk>/delete/', MailingRecipientDeleteView.as_view(), name='recipient_delete'),
    path('message/message_list/', MailingMessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MailingMessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MailingMessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MailingMessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MailingMessageDeleteView.as_view(), name='message_delete'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/<int:pk>/send/', MailingSendView.as_view(), name='mailing_send'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm_email/<uidb64>/<token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('registration_complete/', TemplateView.as_view(template_name="mailing_service/registration_complete.html"),
         name='registration_complete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('statistics/', statistics_view, name='statistics'),
    path('mailing-attempts/', MailingAttemptListView.as_view(), name='mailing_attempt_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
