import csv
import json
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.models import Q

from news.models import Address, KeyWord, Service, Stream
from news_bot.settings import BASE_DIR

path = BASE_DIR / 'fixtures'


def csv_to_json(filename):
    """Making json from csv data."""
    with open(filename, 'r', encoding='utf-8-sig') as csv_file:
        reader = csv.reader(csv_file, delimiter=';', quotechar='"')
        keys = next(reader)
        with open(f'{filename[:-3]}json', 'w', encoding='utf-8') as json_file:
            json_file.write(
                json.dumps(
                    [{key: val for key, val in zip(keys, prop)} for prop in reader],
                    ensure_ascii=False,
                )
                .encode('utf-8')
                .decode()
                .replace('\u200b', '')
            )


def file_handler(name):
    filename = os.path.join(path, f'{name}.csv')
    filename_json = filename[:-3] + 'json'
    if not Path(filename_json).exists() or True:
        csv_to_json(filename)
    return filename_json


def row_handler(row, column):
    value = row.get(column)
    if value:
        return value.replace('\u200B', '')
    return None


class Command(BaseCommand):
    help = 'Загрузка стримов, сервисов и адресов в БД'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--company',
            choices=['mailru', 'rustore'],
            help='Выберите компанию, для которой будет заполнена база',
        )

    def handle(self, *args, **options):
        companies = options.get('company') or ['mailru', 'rustore']
        for company in list(companies):
            for db_file in (f'services_{company}', f'sources_{company}'):
                with open(file_handler(db_file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for row in data:
                        if db_file.startswith('services'):
                            stream, _ = Stream.objects.get_or_create(
                                name=row_handler(row, 'stream'), company=company
                            )
                            key_words = []
                            for kw_type in ('key_word', 'add_key_word', 'blacklist'):
                                kws = row_handler(row, kw_type)
                                if kws:
                                    for kw in kws.split(', '):
                                        kw, _ = KeyWord.objects.get_or_create(
                                            name=kw, kw_type=kw_type
                                        )
                                        key_words.append(kw)
                            service, _ = Service.objects.get_or_create(
                                stream=stream,
                                name=row_handler(row, 'service'),
                            )
                            service.key_words.add(*key_words)
                        elif db_file.startswith('sources'):
                            service = row_handler(row, 'service')
                            stream = row_handler(row, 'stream')
                            if not service:
                                for service in Service.objects.filter(
                                    ~Q(name='Не определен')
                                    & ~Q(name__contains='стартапы'),
                                    stream__name=stream,
                                ):
                                    Address.objects.get_or_create(
                                        address=row_handler(row, 'url'),
                                        search_key_words=True,
                                        service=service,
                                    )
                            else:
                                search_key_words = (
                                    row_handler(row, 'search_key_words') or False
                                )
                                service, _ = Service.objects.get_or_create(
                                    stream=Stream.objects.get(name=stream), name=service
                                )
                                address, _ = Address.objects.get_or_create(
                                    address=row_handler(row, 'url'),
                                    service=service,
                                )
                                address.search_key_words = search_key_words
                                address.search_add_key_words = search_key_words
                                address.save()

        with open(file_handler('key_words'), 'r', encoding='utf-8') as f:
            data = json.load(f)
            for row in data:
                KeyWord.objects.get_or_create(
                    name=row_handler(row, 'name'), kw_type=row_handler(row, 'kw_type')
                )
