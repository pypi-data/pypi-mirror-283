import calendar
import datetime as dt
import json
import locale
import logging
import re
import sys
import traceback
from itertools import chain
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup as Bs
from django.db.models import Q
from django.utils import timezone as tz
from googletrans import Translator

from news.functions import raw_text
from news.models import Address, KeyWord, News


class LocaleManager:
    def __init__(self, localename):
        self.name = localename

    def __enter__(self):
        self.orig = locale.setlocale(locale.LC_CTYPE)
        locale.setlocale(locale.LC_ALL, self.name)

    def __exit__(self, exc_type, exc_value, traceback):
        locale.setlocale(locale.LC_ALL, self.orig)


def coda_handler(news_item):
    with LocaleManager('en_US'):
        pub_date = dt.datetime.strptime(
            str(tz.now().day) + news_item.css('div:nth-child(1) span::text').get(),
            '%d%B %Y',
        )
    names = news_item.css('.kr-cell:nth-child(2) ::text').getall()
    descs = news_item.css('.kr-cell:nth-child(3) ::text').getall()
    title = ', '.join(names)
    text = '\n\t' + '\n\t'.join(': '.join(text_item) for text_item in zip(names, descs))
    return {'pub_date': pub_date, 'title': title, 'text': text}


def mi_handler(news_item):
    news_id = re.search(
        r'"material_id":"(\d*)"', news_item['assembly_info'][0]['extended']
    ).group(1)
    item_url = 'https://go.buy.mi.com/global/discovery/land?id=' + news_id
    mi = json.loads(requests.get(item_url).text)['data']
    title, summary = mi['title'], mi['desc']
    pub_date = dt.datetime.fromtimestamp(int(mi['add_time'])).date()
    text = Bs(mi['content'], 'lxml').get_text()
    return {'pub_date': pub_date, 'title': title, 'summary': summary, 'text': text}


def todoist_news_handler(news):
    html = (
        json.loads(news.css('::text').get())['props']['pageProps']['article']['body']
        .replace('<div class="box-tip">', '</article><div class="box-tip">')
        .replace('</h2>', '</h2><article>')
        .replace('<h2>', '</article><h2>')
        .replace('</article>', '', 1)
    )
    soup = Bs(html, 'lxml')
    news = []
    for h2, article in zip(soup.find_all('h2'), soup.find_all('article')):
        title = h2.string
        pub_date = re.search(r': (\d{1,2} [А-Яа-я]{3})', title)
        if pub_date:
            with LocaleManager('ru_RU'):
                try:
                    pub_date = dt.datetime.strptime(
                        pub_date.group(1) + str(tz.now().year), '%d %b%Y'
                    )
                except ValueError:
                    logging.error(f'Could not parse date: {pub_date}')
                    continue
                if pub_date > tz.now():
                    pub_date = tz.datetime(
                        pub_date.year - 1, pub_date.month, pub_date.day
                    ).date()
            news.append(
                {
                    'pub_date': pub_date,
                    'title': title,
                    'text': article.get_text().strip('\n').replace('\xa0', ''),
                }
            )
    return news


def ticktick_news_handler(news):
    for i, news_item in enumerate(news):
        if not news_item.css(':has(span.label-new)') and (
            not news_item.css(':has(span.label-improved)')
        ):
            news_item.pop(i)
    return news


def support_google_news_handler(response):
    date = response.css(':is(h2, h3) ::text').get()
    news = []
    flag = False
    for news_item in response:
        if news_item.css('.no-margin h3') and 'play' in (
            news_item.css('.no-margin h3 ::text').get().lower()
        ):
            news.append(
                {
                    'pub_date': tz.now().date(),
                    'title': f'{news_item.css("h3 ::text").get()} ({date})',
                    'text': news_item.css('ul').get(),
                }
            )
            flag = True
        elif flag:
            if news_item.css('.no-margin'):
                break
            else:
                try:
                    news[-1]['text'] += news_item.get()
                except Exception:
                    pass
    return news


def support_microsoft_news_handler(response):
    date_pattern = r'Version ([\d]{2})([\d]{2}): ([A-Za-z]+) ([\d]{2})'
    news = []
    flag = False
    for news_item in response:
        if news_item.css('h2'):
            item = {
                'text': '',
                'url': '#' + news_item.css('h2::attr(id)').get(),
                'title': news_item.css('h2::text').get(),
            }
            date = news_item.css('h2::text').re(date_pattern)
            if not date:
                continue
            y, m1, m2, d = date
            m2 = dt.datetime.strptime(m2, '%B').month
            y = dt.datetime.strptime(
                str(int(y) + 1 if int(m1) > m2 else int(y)), '%y'
            ).year
            item['pub_date'] = dt.date(y, m2, int(d))
            flag = True
            news.append(item)
        elif news_item.css('.NOTE'):
            flag = False
        elif flag:
            news[-1]['text'] += news_item.get()
    return news


def text_date(x, fmt='%d %b %Y', sep=','):
    lang = 'ru_RU' if re.search(r'[А-Яа-я]+', x) else 'en_US'
    with LocaleManager(lang):
        if (
            'назад' in x
            or re.search(r'[Сс]егодня', x)
            or 'ago' in x
            or (re.search(r'[Tt]oday', x))
        ):
            return tz.now().strftime(fmt)
        if re.search(r'[Вв]чера', x) or re.search(r'[Yy]esterday', x):
            return (tz.now() - tz.timedelta(days=1)).strftime(fmt)

    seps = [',', ' at']
    for sep in seps:
        if sep in x:
            if not re.search(r'\d{4}', x):
                return x.split(sep)[0] + ' ' + str(tz.now().year)
            return x.split(sep)[0]
    return x


def convert_response(response):
    def replace(m):
        return m.group(1) + '\U0001F910' + m.group(2)

    return (
        (
            '{'
            + re.search(
                r'\\"versionHistory\\":\[[^\]]*\]',
                re.sub(
                    r'([^\}])\]([^,])',
                    replace,
                    response.css('#shoebox-media-api-cache-apps::text').get(),
                ),
            ).group()
            + '}'
        )
        .replace('\\\"', '"')
        .replace('\\\\\"', '\u2019\u2019')
        .replace('\\\\', '\\')
        .replace('\'', '\u2019')
    )


def convert_url(url):
    months = (
        '',
        'january',
        'february',
        'march',
        'april',
        'may',
        'june',
        'july',
        'august',
        'september',
        'october',
        'november',
        'december',
    )

    def dropbox_converting(timedelta):
        try:
            d_now = tz.now().date() - tz.timedelta(days=30 * timedelta)
            source = url.strip('/') + f'/dbx-{months[d_now.month]}-{d_now.year}'
            return requests.get(source, timeout=30).status_code, source
        except Exception:
            return 404, None

    if 'https://www.data.ai/' in url:
        url = (
            url.replace('timeline', 'events').replace('details', 'events').split('?')[0]
        )
        return urljoin(
            'https://api.data.ai/', 'v1.3' + re.search('data.ai(.*)', url).group(1)
        )
    if 'https://blog.google' in url:
        url = url.replace('products/', 'api/v2/latest?tags=')
        url = url.strip('/')
        if 'gmail' in url:
            return url.replace('gmail', 'inbox,gmail')
        if 'docs' in url:
            return url.replace('docs', 'sheets,sites,slides,docs,forms,keep')
    if 'https://www.mi.com/global/discover/newsroom' in url:
        return url.replace('www', 'go.buy').replace(
            'discover/', 'page/discovery?from=mobile&show_type='
        )
    if 'https://amazonphotos.blog' in url:
        return url.replace('.blog', '.medium.com')
    if 'support-google-com.translate.goog' in url:
        return url.replace('support-google-com.translate.goog', 'support.google.com')
    if 'https://www.vedomosti.ru/technologies' in url:
        try:
            return urljoin(
                url,
                Bs(requests.get(url).text, 'lxml').select('.release__button')[0][
                    'href'
                ],
            )
        except Exception:
            pass
    if 'https://www.dropbox.com/product-updates' in url:
        status_code, source = dropbox_converting(0)
        counter = 1
        while status_code == 404 and counter < 12:
            status_code, source = dropbox_converting(counter)
            counter += 1
        return source
    return url


def search(item, addresses):
    def search_key_words(address, text, soup_text):
        if re.search(
            r'\/\/apps\.apple\.com|www\.data\.ai|sj\.360\.cn\/changelog\.htm',
            address.address,
        ):
            for block_phrase in KeyWord.objects.filter(kw_type='blocklist'):
                if block_phrase.name == soup_text:
                    return False
            if re.search(r'bug fixes|improvements', soup_text[:70].lower()):
                return False
            return True
        service = address.service
        kw_search, kw_add_search = (
            address.search_key_words,
            address.search_add_key_words,
        )
        kw_types = []
        if not kw_search:
            kw_types.append('key_word')
            kw_types.append('blacklist')
        if not kw_add_search:
            kw_types.append('add_key_word')
        key_words = service.key_words.filter(~Q(kw_type__in=kw_types))
        if not key_words:
            return True
        kws = [
            kw.get_kw_forms()
            for kw in (key_words.filter(kw_type__in=('key_word', 'add_key_word')))
        ]
        blacklist = [
            kw.get_kw_forms() for kw in (key_words.filter(kw_type='blacklist'))
        ]
        for bl in chain(*blacklist):
            if bl in text:
                text = text.replace(bl, '')
        for key_word in chain(*kws):
            if key_word in text:
                return True
        return False

    addresses_count = len(addresses)
    soup_text = raw_text(item.get('text')) if item.get('text') else ''
    text = (
        (item.get('title') or '').lower()
        + (item.get('summary') or '').lower()
        + soup_text.lower()
    )
    for address_item in addresses:
        if search_key_words(address_item, text, soup_text):
            item['is_blacklisted'] = False
            item['address'] = address_item
            if not News.objects.filter(
                address__service__stream=address_item.service.stream,
                is_blacklisted=False,
                text=raw_text(item.get('text')),
            ) or not item.get('text'):
                yield item
        else:
            company = address_item.service.stream.company
            main_qs = News.objects.filter(
                address__address__contains=address_item.address,
                address__service__stream__company=company,
                is_blacklisted=False,
            )
            if (
                (item.get('text') and main_qs.filter(text=raw_text(item.get('text'))))
                or item.get('title')
                and main_qs.filter(title=item.get('title'))
            ):
                continue
            item['is_blacklisted'] = True
            item['address'] = (
                Address.get_not_defined(
                    address_item.address, address_item.service.stream.company
                )
                if addresses_count > 1
                else address_item
            )
            yield item


class ParseHandler:
    def __init__(self, parse_data, item_or_details='item'):
        self.data = parse_data
        self.item_or_details = item_or_details
        self.item = {}
        self.translator = Translator(
            service_urls=[
                'translate.google.com',
            ]
        )

    def get_fields(self, response, parse_date=True):
        if self.data.get(self.item_or_details):
            for field, tag in self.data[self.item_or_details].items():
                if field == 'pub_date' and not parse_date:
                    continue
                if field == 'script':
                    self.item.update(tag(response))
                elif (
                    self.data.get('api') or self.data.get('api_like')
                ) and self.item_or_details == 'item':
                    self.item[field] = response[tag]
                    if self.item[field] and isinstance(self.item[field], str):
                        self.item[field] = self.item[field].replace('\U0001F910', ']')
                elif self.data.get('bs4'):
                    try:
                        if field == 'text':
                            self.item[field] = ''.join(
                                [str(i) for i in response.select(tag)]
                            )
                        else:
                            self.item[field] = (
                                (response.select(tag)[0].get_text())
                                if isinstance(tag, str)
                                else (response.select(tag[0])[0][tag[1]])
                            )
                    except Exception:
                        self.item[field] = None
                    try:
                        self.item[field] = self.item[field].strip()
                    except Exception:
                        pass
                else:
                    self.item[field] = response if tag == '' else (response.css(tag))
                    if field == 'summary':
                        self.item[field] = Bs(
                            ''.join(self.item[field].getall()), 'lxml'
                        ).get_text()
                    elif field == 'text':
                        self.item[field] = ''.join(self.item[field].getall())
                    else:
                        self.item[field] = self.item[field].get()
                    if self.item[field]:
                        self.item[field] = self.item[field].strip()
                if field == 'pub_date' and not self.data.get('api_like'):
                    self.item[field] = self.get_date(
                        self.item[field], self.data.get('format'), self.data.get('lang')
                    )
                if field in ('title', 'summary', 'text'):
                    self.item[field] = self.translate(
                        self.item[field],
                        field,
                        self.data.get('translate'),
                    )
        return self.item

    def get_date(self, date, format=None, lang=None):
        def replace(m):
            return m.group()[:3]

        if not date:
            return None
        if self.data.get('pub_date_formatting'):
            date = self.data['pub_date_formatting'](date)
        if isinstance(date, dt.date):
            return date
        if lang and lang.startswith('ru'):
            date = date.lower()
            date = re.sub('[а-я]+', replace, date)
            with LocaleManager(lang or 'ru_RU'):
                if 'мая' in date and not ('мая' in list(calendar.month_abbr)):
                    date = date.replace('мая', 'май').strip()
                elif 'май' in date and not ('май' in list(calendar.month_abbr)):
                    date = date.replace('май', 'мая').strip()
            format = format.replace('B', 'b')
        if format:
            if lang != 'ru_RU' and re.search(r'[А-Яа-я]+', date):
                lang = 'ru_RU'
            with LocaleManager(lang or 'en_US'):
                return dt.datetime.strptime(date, format).date()
        return dt.datetime.strptime(date.split('T')[0], '%Y-%m-%d').date()

    def translate(self, item, field, translation_needed=None):
        def repl(m):
            try:
                return self.translator.translate(m.group()).text
            except Exception:
                return m.group()

        def replace(m):
            flag = False
            if not isinstance(m, str):
                m = m.group(1)
                flag = True
            if len(m) > 1000:
                if flag:
                    return '>' + re.sub(r'[^,\.\nA-Za-zА-Яа-я]+', repl, m) + '<'
                return re.sub(r'[^,\.\nA-Za-zА-Яа-я]+', repl, m)
            try:
                m = self.translator.translate(m).text
            except Exception:
                pass
            if flag:
                return '>' + m + '<'
            return m

        if translation_needed and item:
            try:
                if field == 'text':
                    item = item.replace('\u200C', '')
                    return re.sub(r'>([^<>]+)<', replace, item)
                return replace(item)
            except Exception as e:
                logging.error(
                    f'Translation was not successfull: {e}\n'
                    f'{traceback.format_exc()}'
                    f'{sys.exc_info()[2]}'
                    f'"{item}"'
                )
        return item
