from django.core.management.base import BaseCommand
from mailing_service.models import Mailing


class Command(BaseCommand):
    help = 'Отправка всех рассылок со статусом "created"'

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status='created')
        for mailing in mailings:
            mailing.send()
            self.stdout.write(f'Рассылка {mailing.pk} отправлена.')