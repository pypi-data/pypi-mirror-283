from django.core.management.base import BaseCommand

from news.models import Address, KeyWord, News, Service, Stream


# Scrapy container better be stopped before executing this command.
# Web container should be restarted after executing this command.
class Command(BaseCommand):
    help = (
        'Очистка базы для перезапуска проекта. '
        'По умолчанию удаляются только непрошедшие модерацию новости.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '-d', '--delete-all', action='store_true', help='Удалить все сущности'
        )

    def handle(self, *args, **options):
        if options['delete_all']:
            News.objects.all().delete()
            Address.objects.all().delete()
            Service.objects.all().delete()
            Stream.objects.all().delete()
            KeyWord.objects.all().delete()
        else:
            News.objects.filter(is_moderated=False).delete()
