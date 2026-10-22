from django.core.management.base import BaseCommand

from materials.reminders import lessons_soon, send_due_reminders


class Command(BaseCommand):
    help = 'Надіслати в Telegram нагадування (ДЗ, кінець підписки, покинута практика, заняття), яких ще не надсилали'

    def handle(self, *args, **options):
        self.stdout.write(f'Надіслано нагадувань: {send_due_reminders() + send_due_reminders(lessons_soon())}')
