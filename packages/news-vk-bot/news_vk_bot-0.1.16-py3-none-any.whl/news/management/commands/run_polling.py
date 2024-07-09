from django.core.management.base import BaseCommand

from news.handlers.dispatcher import run_polling


class Command(BaseCommand):
    help = 'Запуск бота в polling режиме'

    def handle(self, *args, **options):
        run_polling()
