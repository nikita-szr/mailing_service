from django.urls import path
from .views import (
    MailingRecipientListView,
    MailingRecipientDetailView,
    MailingRecipientCreateView,
    MailingRecipientUpdateView,
    MailingRecipientDeleteView,
    MailingMessageListView,
    MailingMessageDetailView,
    MailingMessageCreateView,
    MailingMessageUpdateView,
    MailingMessageDeleteView,
    MailingListView,
    MailingDetailView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingSendView
)
from django.conf import settings
from django.conf.urls.static import static


app_name = 'mailing_service'

urlpatterns = [
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)