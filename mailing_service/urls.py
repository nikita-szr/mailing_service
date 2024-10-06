from django.urls import path
from .views import (MailingRecepientListView, MailingRecepientDetailView, MailingRecepientCreateView,
                    MailingRecepintUpdateView, MailingRecepientDeleteView)

urlpatterns = [
    path('', MailingRecepientListView.as_view(), name='recepient_list'),
    path('recepient/<int:pk>/', MailingRecepientDetailView.as_view(), name='recepient_detail'),
    path('recepient/create', MailingRecepientCreateView.as_view(), name='recepient_create'),
    path('recepient/<int:pk>/update/', MailingRecepintUpdateView.as_view(), name='recepient_update'),
    path('recepient/<int:pk>/delete/', MailingRecepientDeleteView.as_view(), name='recepient_delete'),
]
