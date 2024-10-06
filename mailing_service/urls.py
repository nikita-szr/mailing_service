from django.urls import path
from .views import (
    MailingRecipientListView,
    MailingRecipientDetailView,
    MailingRecipientCreateView,
    MailingRecipientUpdateView,
    MailingRecipientDeleteView
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)