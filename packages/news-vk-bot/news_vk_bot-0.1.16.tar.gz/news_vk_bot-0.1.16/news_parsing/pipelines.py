import logging
import os
import time

from django.core.exceptions import ValidationError
from django.utils import timezone as tz
from dotenv import load_dotenv

from news.functions import raw_text
from news.models import Address, News
from news_parsing.feeds import stat
from news_parsing.models import Parsing
from news_parsing.validators import unique_vc

load_dotenv()

HOURS = int(os.getenv('SCRAPY_PERIOD', 6)) * 3600


class NewsParsingPipeline:
    def __init__(self):
        self.parsing = Parsing()
        self.last_parsing = (
            Parsing.objects.latest('id') if (Parsing.objects.all()) else None
        )

    def open_spider(self, spider):
        if self.last_parsing and (
            tz.now().date() - self.last_parsing.last_log_renewal
        ) > tz.timedelta(days=3):
            os.remove(
                os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    'err.log',
                )
            )
            self.parsing.last_log_renewal = tz.now().date()
        else:
            self.parsing.last_log_renewal = (
                (self.last_parsing.last_log_renewal)
                if self.last_parsing
                else tz.now().date()
            )
        logging.warning('Starting to crawl...')
        self.parsing.last_start = tz.now()

    def close_spider(self, spider):
        if Address.objects.all():
            self.parsing.last_end = tz.now()
            logging.warning(
                f'Crawling is done. Waiting {HOURS / 3600} hours '
                'for the next time...'
            )
            self.parsing.save()
            stat()
            time.sleep(HOURS)
        else:
            logging.warning('Nothing to parse')
            time.sleep(30)

    def process_item(self, item, spider):
        return process_item(item)


def process_item(item, do_return=True):
    item['stream'] = item['address'].service.stream
    try:
        item.instance.full_clean()
        if not unique_vc(item):
            raise ValidationError('not unique vc.ru news item')
        item.save()
        if item['is_blacklisted'] is False:
            same_but_blacklisted = News.objects.filter(
                address=Address.get_not_defined(
                    address_address=item['address'].address,
                    company=item['address'].service.stream.company,
                ),
                is_blacklisted=True,
                title=item.get('title'),
                text=raw_text(item.get('text')),
            )
            if same_but_blacklisted:
                same_but_blacklisted.delete()
        if do_return:
            return 'saved'
    except ValidationError:
        pass
    # except ValidationError as e:
    #     return logging.error(f'{item["url"]}: {e}')
