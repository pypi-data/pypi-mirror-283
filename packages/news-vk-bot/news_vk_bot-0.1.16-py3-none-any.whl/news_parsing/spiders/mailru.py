import datetime as dt
import json
import logging
import warnings
from urllib.parse import urljoin

import requests
import scrapy
from bs4 import BeautifulSoup as Bs

from news.models import Address

from ..items import NewsItem
from ..pipelines import process_item
from .constants import SOURCES
from .handlers import ParseHandler, convert_url, search

warnings.filterwarnings(action='ignore', category=UserWarning)


class MailruSpider(scrapy.Spider):
    name = 'mailru'
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    handler.setFormatter(
        logging.Formatter(fmt='%(asctime)s [%(name)s] %(levelname)s: %(message)s')
    )
    logging.getLogger().addHandler(handler)

    def start_requests(self):
        for address in set(
            Address.objects.filter(for_parser=True).values_list('address', flat=True)
        ):
            parse_data = {}
            url = convert_url(address)
            for source in SOURCES:
                if url.startswith(source):
                    parse_data = SOURCES[source]
            if not parse_data or parse_data.get('forbidden'):
                continue
            meta = {'parse_data': parse_data, 'address': address}
            if parse_data.get('bs4'):
                try:
                    req = requests.get(url).text
                except Exception as e:
                    logging.error(f'{url}: {e}')
                    continue
                if parse_data.get('broken_code'):
                    req = req.replace('</body></html>', '') + '</body></html>'
                soup = Bs(req, 'lxml')
                news = soup.select(parse_data['news'])
                for news_item in news:
                    try:
                        item_url = urljoin(
                            url, news_item.select(parse_data.get('url'))[0]['href']
                        )
                        item = {'url': item_url}
                        item.update(ParseHandler(parse_data).get_fields(news_item))
                        try:
                            try:
                                req = requests.get(item_url).text
                            except Exception as e:
                                logging.error(f'{item_url}: {e}')
                                continue
                            if parse_data.get('broken_code'):
                                req = req.replace('</body></html>', '') + (
                                    '</body></html>'
                                )
                            soup_item = Bs(req, 'lxml')
                            item.update(
                                ParseHandler(parse_data, 'details').get_fields(
                                    soup_item
                                )
                            )
                        except Exception as e:
                            logging.error(f'[{item_url}]: {e}')
                        if item.get('pub_date') is not None:
                            items = search(
                                item,
                                Address.objects.filter(
                                    address=address, for_parser=True
                                ),
                            )
                            for it in items:
                                process_item(NewsItem(it), False)
                    except Exception as e:
                        logging.error(f'[{url}]: {e}')
                continue
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta=meta,
                headers=parse_data.get('headers'),
            )

    def parse(self, response):
        address = response.meta.get('address')
        parse_data = response.meta.get('parse_data')
        if parse_data:
            api = parse_data.get('api')
            api_like = parse_data.get('api_like')
            if api:
                response_news = (
                    parse_data['script'](response)
                    if (parse_data.get('script'))
                    else response.text
                )
                response_news = json.loads(response_news)
            news = (
                response_news[parse_data['news']]
                if api
                else (response.css(parse_data['news']))
            )
            if parse_data.get('news_formatting'):
                if news is not None:
                    news = parse_data['news_formatting'](news)
            required = parse_data.get('required')
            for news_item in news:
                if required and (news_item[required['key']] != required['value']):
                    continue
                url = parse_data.get('url')
                if url:
                    url = (
                        news_item.get(url)
                        if (api or api_like)
                        else (news_item.css(url).get())
                    )
                    if parse_data.get('url_formatting'):
                        url = parse_data['url_formatting'](url)
                url = urljoin(address, url)
                item = {'url': url}
                try:
                    if parse_data.get('root_pub_date'):
                        item['pub_date'] = ParseHandler(parse_data).get_date(
                            response.css(parse_data['root_pub_date']).get(),
                            format=parse_data.get('format'),
                        )
                    item.update(ParseHandler(parse_data).get_fields(news_item))
                    if url.endswith('.pdf') and not item.get('text'):
                        item['text'] = ''
                    addresses = Address.objects.filter(address=address, for_parser=True)
                    if item.get('text') is not None:
                        if api and not item['text']:
                            continue
                        items = search(item, addresses)
                        for item in items:
                            yield NewsItem(item)
                    else:
                        yield response.follow(
                            url=item['url'],
                            callback=self.parse_details,
                            cb_kwargs=dict(
                                item=item, parse_data=parse_data, addresses=addresses
                            ),
                        )
                except Exception as e:
                    logging.error(f'[{url}]: {e}')

    def parse_details(self, response, item, parse_data, addresses):
        try:
            parse_date = (
                False
                if parse_data['details'].get('pub_date')
                and (item.get('pub_date') and isinstance(item['pub_date'], dt.date))
                else True
            )
            item.update(
                ParseHandler(parse_data, 'details').get_fields(response, parse_date)
            )
            if item.get('pub_date') is not None:
                items = search(item, addresses)
                for item in items:
                    yield NewsItem(item)
        except Exception as e:
            logging.error(f'[{item.get("url")}]: {e}')
