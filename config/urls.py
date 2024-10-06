from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("mailing_service/", include("mailing_service.urls", namespace="mailing_service"))
]
