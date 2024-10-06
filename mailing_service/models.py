from django.db import models


class MailingRecipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email
