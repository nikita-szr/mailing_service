from django.db import models
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class MailingRecipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipients')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        ordering = ['full_name']


class MailingMessage(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['subject']


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_datetime = models.DateTimeField("Дата и время начала отправки", default=timezone.now)
    end_datetime = models.DateTimeField("Дата и время окончания отправки", blank=True, null=True)
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey('MailingMessage', on_delete=models.CASCADE, related_name='mailings')
    recipients = models.ManyToManyField('MailingRecipient', related_name='mailings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mailings')

    def __str__(self):
        return f'Рассылка {self.pk} - {self.status}'

    def send(self):
        """Отправка сообщений всем получателям и логирование попыток отправки"""
        if self.status != 'created':
            return

        recipients = self.recipients.all()
        emails = [recipient.email for recipient in recipients]

        for recipient in recipients:
            try:
                send_mail(
                    subject=self.message.subject,
                    message=self.message.body,
                    from_email='test@test.com',
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )

                MailingAttempt.objects.create(
                    mailing=self,
                    status='success',
                    server_response='Письмо отправлено успешно.',
                    attempt_datetime=timezone.now()
                )

            except BadHeaderError as e:
                MailingAttempt.objects.create(
                    mailing=self,
                    status='failure',
                    server_response=str(e),
                    attempt_datetime=timezone.now()
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=self,
                    status='failure',
                    server_response=str(e),
                    attempt_datetime=timezone.now()
                )

        self.status = 'started'
        self.start_datetime = timezone.now()
        self.save()


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failure', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    attempt_datetime = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Попытка рассылки {self.mailing} - {self.get_status_display()}"


class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username
