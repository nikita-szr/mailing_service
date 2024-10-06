from django.db import models
from django.utils import timezone


class MailingRecipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    comment = models.TextField(blank=True, null=True)

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

    def __str__(self):
        return f'Рассылка {self.pk} - {self.status}'
