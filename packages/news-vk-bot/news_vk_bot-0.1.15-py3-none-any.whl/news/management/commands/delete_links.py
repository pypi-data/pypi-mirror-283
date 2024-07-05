from django.core.management.base import BaseCommand

from news.models import News


class Command(BaseCommand):
    help = 'Удаление всех ссылок из новостей.'

    def handle(self, *args, **options):
        for news_item in News.objects.all():
            news_item.save()
