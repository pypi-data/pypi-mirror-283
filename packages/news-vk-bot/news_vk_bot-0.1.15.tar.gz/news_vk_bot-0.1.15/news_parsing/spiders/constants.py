import datetime as dt
import json
import os
import re

from django.utils import timezone as tz
from dotenv import load_dotenv

from .handlers import (coda_handler, convert_response, mi_handler,
                       support_google_news_handler,
                       support_microsoft_news_handler, text_date,
                       ticktick_news_handler, todoist_news_handler)

load_dotenv()

DATAAI_API_KEY = os.getenv('DATAAI_API_KEY')


def repl(m):
    return m.group()[:3]


SOURCES = {
    'https://api.data.ai': {
        'api': True,
        'headers': {'Authorization': f'Bearer {DATAAI_API_KEY}'},
        'news': 'data',
        'required': {'key': 'event_type', 'value': 'version_change'},
        'item': {'pub_date': 'date', 'title': 'new_value', 'text': 'release_note'},
        'format': '%Y-%m-%d',
    },
    'https://apps.apple.com/': {
        'script': convert_response,
        'api': True,
        'news': 'versionHistory',
        'item': {
            'pub_date': 'releaseTimestamp',
            'title': 'versionDisplay',
            'text': 'releaseNotes',
        },
    },
    'https://yandex.ru/blog/': {
        'news': 'div[data-block=b-post]',
        'url': 'a[class*=title]::attr(href)',
        'item': {'title': 'div[class*=title]::text', 'summary': 'div[class*=text]'},
        'details': {
            'pub_date': 'div[itemprop=datePublished]::attr(content)',
            'text': 'section[itemprop=articleBody] > *',
        },
    },
    'https://blog.google': {
        'api': True,
        'news': 'results',
        'url': 'full_url',
        'item': {
            'title': 'headline',
            'pub_date': 'published',
            'summary': 'summary',
        },
        'details': {'text': 'section.article-container > *'},
    },
    'https://workspaceupdates.googleblog.com': {
        'news': '.post',
        'url': '.title > a::attr(href)',
        'item': {
            'title': '.title > a::text',
            'pub_date': '[itemprop=datePublished]::text',
            'text': '[itemprop=articleBody] *:is(h3, div)',
        },
        'format': '%A, %B %d, %Y',
    },
    'https://techcommunity.microsoft.com/': {
        'news': 'div[class*=blog-message] > div[class*=row-main]',
        'url': 'h1.message-subject > span > a::attr(href)',
        'item': {
            'title': 'h1.message-subject > span > a::text',
            'summary': '.blog-article-teaser-wrapper',
            'pub_date': '.author-details > span:nth-child(3)::text',
        },
        'details': {
            'text': '.lia-message-body-content',
        },
        'format': '%b %d %Y %H:%M %p',
    },
    'https://www.microsoft.com/en-us/microsoft-365/blog': {
        'news': 'article[id]',
        'url': '.card__link::attr(href)',
        'item': {
            'title': '.card__link span:nth-child(1)::text',
            'summary': '.card__content > *:not(:is(div, h3))',
            'pub_date': '.card__date time::attr(datetime)',
        },
        'details': {
            'text': ':is(.single__content, .entry_content, .entry-content) > *:not(:is(div, figure, hr))',
        },
    },
    'https://www.yahooinc.com/press-releases': {
        'news': 'div[role=listitem]',
        'url': 'a::attr(href)',
        'item': {
            'title': 'h2::text',
            'pub_date': 'div[class=tags-categories]::text',
        },
        'details': {
            'text': '.collection-content p',
        },
        'format': '%B %d, %Y',
    },
    'https://www.apple.com/newsroom': {
        'news': 'li.tile-item',
        'url': 'a::attr(href)',
        'item': {
            'title': 'div.tile__headline::text',
            'pub_date': 'div.tile__timestamp::attr(data-ts)',
        },
        'details': {
            'summary': '.article-subhead > div',
            'text': '.pagebody *[class*=pagebody]',
        },
    },
    'https://www.gmx.net/mail/updates': {
        'news': 'div[class*=article]',
        'url': 'div.description > a:last-child::attr(href)',
        'item': {
            'title': 'h2::text',
            'summary': 'div.description',
            'pub_date': 'aside::text',
        },
        'details': {
            'text': ':is(#articlecomplete, [data-cc=section])',
        },
        'format': '%d. %B %Y',
        'lang': 'de_DE',
        'translate': True,
    },
    'https://news.rambler.ru/theme/': {
        'bs4': True,
        'news': 'div[data-blocks*=news_list]',
        'url': 'h2 > a',
        'item': {
            'title': 'h2 > a > span',
        },
        'details': {
            'summary': '#summary',
            'text': '[id*=cluster] div:has(> #summary) p',
            'pub_date': ['[property="og:pubdate"]', 'content'],
        },
        'pub_date_formatting': lambda x: x.upper(),
    },
    'https://www.zoho.com/blog/': {
        'news': 'article',
        'url': 'h2.blog-title > a::attr(href)',
        'item': {
            'title': 'h2.blog-title > a::text',
            'pub_date': 'time[class*=published]::attr(datetime)',
        },
        'details': {
            'text': '.entry-content > *',
        },
        'format': '%y-%m-%dIST%H:%M:%S%z',
    },
    'https://blog.zoom.us': {
        'news': 'div[class*=post-card]',
        'url': '.card-title > a::attr(href)',
        'item': {
            'title': '.card-title > a::text',
            'pub_date': 'div.details > div:first-child::text',
        },
        'details': {
            'text': '.article > *:is(p, ul, h2)',
        },
        'format': '%B %d, %Y',
    },
    'https://myoffice.ru/press-center/produktyi': {
        'news': '.news-main__list-col',
        'url': 'a::attr(href)',
        'item': {
            'title': '.news-main__list-title::text',
            'pub_date': '.news-main__list-date::text',
        },
        'details': {
            'text': '[itemprop=articleBody]',
        },
        'format': '%d %B %Y',
        'lang': 'ru_RU',
    },
    'http://research.baidu.com/Blog': {
        'news': '.blog > li',
        'url': 'a::attr(href)',
        'item': {
            'title': '.blog-title::text',
            'summary': '.blog-introduce',
            'pub_date': '.blog-date::text',
        },
        'details': {
            'text': '.container-details-er > p',
        },
        'pub_date_formatting': lambda x: re.sub(
            'st|nd|rd|th|',
            '',
            x + str(tz.now().year) if not re.search(r'\d{4}', x) else x,
        ).replace('\uff0c', ', '),
        'format': '%b %d, %Y',
    },
    'https://www.tencent.com/en-us/media/news.html?type=media': {
        'news': '[class*=block1] [class*=item]',
        'url': 'a::attr(href)',
        'item': {
            'title': 'h3::text',
            'summary': 'p',
            'pub_date': '[class*=tagline]::text',
        },
        'details': {
            'text': '.text > p',
        },
        'format': '%Y.%m.%d',
    },
    'https://blogs.microsoft.com': {
        'news': 'article',
        'url': '.f-post-link::attr(href)',
        'item': {'title': 'h3::text', 'pub_date': 'time::attr(datetime)'},
        'details': {
            'text': '[class*=entry-content] > p',
        },
        'format': '%Y-%m-%d',
    },
    'https://blog.whatsapp.com': {
        'news': '._aiwh > div',
        'url': 'h1 > a::attr(href)',
        'item': {
            'title': '._9vg3::text',
            'pub_date': '._8l_f:nth-child(2) p::text',
            'text': '._8l_f:nth-child(1) p',
        },
        'format': '%B %d, %Y',
    },
    'https://newsroom.snap.com/ru-RU': {
        'news': '.body-container .css-lznv47',
        'url': 'a::attr(href)',
        'url_formatting': lambda x: (
            x.replace('ru-RU', 'ru-RU/') if 'ru-RU/' not in x else x
        ),
        'details': {
            'title': 'h1 ::text',
            'summary': 'div[class*=background] div:has(h1) div[class*=sdsm-p]',
            'text': 'section[class*=background] div[class*=sdsm-p]',
            'pub_date': 'div.css-1kpisj0::text',
        },
        'pub_date_formatting': lambda x: re.search(
            r'\d{1,2}\s*[а-яА-Яa-zA-z]{3,15}\s*\d{2,4}', x
        ).group(),
        'format': '%d %B %Y',
    },
    'https://telegram.org/blog': {
        'news': 'a[class*=dev_blog_card]',
        'url': '::attr(href)',
        'item': {
            'title': 'h4::text',
            'summary': '.dev_blog_card_lead',
            'pub_date': '.dev_blog_card_date::text',
        },
        'details': {
            'text': '#dev_page_content :is(p, h3, blockquote)',
        },
        'format': '%b %d, %Y',
    },
    'https://weixin.qq.com/cgi-bin/readtemplate?lang=zh_CN&t=weixin_faq': {
        'news': '.faq_list_content li',
        'url': 'a::attr(href)',
        'item': {
            'pub_date': 'span:nth-child(2)::text',
        },
        'details': {
            'title': '.faq_title::text',
            'text': '.content > *:not(.faq_title)',
        },
        'format': '(%Y-%m-%d)',
        'translate': True,
    },
    'https://discord.com/blog': {
        'news': '.blog-featured-section [role=listitem]',
        'url': 'a::attr(href)',
        'item': {
            'title': ':is([class*=title], a[class*=heading])::text',
        },
        'details': {
            'pub_date': '.blog-post-author-name::text',
            'summary': 'meta[name=description]',
            'text': '.blog-post-content > *',
        },
        'format': '%B %d, %Y',
    },
    'https://signal.org/blog': {
        'news': '.blog-post-preview',
        'url': 'h3 a::attr(href)',
        'item': {
            'title': 'h3::text',
            'summary': 'div div:nth-child(2) > div > *',
            'pub_date': 'p.body2',
        },
        'details': {'text': ('.blog-post-content .column > *:not(div)')},
        'pub_date_formatting': lambda x: re.sub('<p .*>.*> on |</p>', '', x),
        'format': '%d %b %Y',
    },
    'https://www.viber.com/en/blog': {
        'news': '[class*=blogroll-post]',
        'url': 'a::attr(href)',
        'item': {'title': 'h3 a::text', 'summary': '*'},
        'details': {'pub_date': '.post-date::text', 'text': '.entry-content > *'},
        'format': '%B %d, %Y',
    },
    'https://www.skype.com/en/blogs': {
        'news': ':is(.ContentPadding, .mainHero) .colContent:not(:empty)',
        'url': 'a::attr(href)',
        'item': {'title': ' :is(h1, h3)::text', 'summary': 'p', 'pub_date': 'div p'},
        'details': {
            'text': '[role=main] .colContent p',
        },
        'pub_date_formatting': lambda x: re.search(r'\d\d\/\d\d\/\d\d\d\d', x).group(),
        'format': '%d/%m/%Y',
    },
    'https://support.microsoft.com/en-us/office/onedrive-release-notes': {
        'news': 'article .supTabControlContent',
        'item': {
            'title': 'h2#ID0EDJBBLDF::text',
            'text': '[aria-labelledby=ID0EDJBBLDF] ul',
            'pub_date': 'div:nth-child(1) p i::text',
        },
        'format': 'Last updated: %B %d, %Y',
    },
    'https://www.dropbox.com/product-updates': {
        'news': 'main#main-content > :has(a):has(p)',
        'url': '',
        'item': {'title': 'h2::text', 'text': '[class*=text] > :not(br)'},
        'root_pub_date': 'title::text',
        'pub_date_formatting': lambda x: tz.now().date(),
    },
    'https://blog.mega.io': {
        'news': '#recent a',
        'url': '::attr(href)',
        'item': {
            'title': '.title::text',
            'summary': '.excerpt',
            'pub_date': '.post-date::text',
        },
        'details': {
            'text': '.content > :not(:is(figure))',
        },
        'format': '%d %b %Y',
    },
    'https://blog.pcloud.com/category/products': {
        'news': '.isotope-container > *',
        'url': 'a::attr(href)',
        'item': {'title': 'h3::text', 'pub_date': '.t-entry-date::text'},
        'details': {
            'text': '.post-content > :not(:is(div))',
        },
        'format': '%B %d, %Y',
    },
    'https://blog.box.com/category/product': {
        'news': '.article-listing--item',
        'url': '::attr(href)',
        'item': {
            'title': 'h6::text',
            'summary': 'p',
            'pub_date': 'time::attr(datetime)',
        },
        'details': {'text': '.paragraph > *'},
        'format': '%Y-%m-%d',
    },
    'https://nextcloud.com/blog': {
        'news': '.news-item',
        'url': 'h4 a::attr(href)',
        'item': {'title': 'h4 a::text', 'summary': 'p', 'pub_date': '.date::text'},
        'details': {'text': '.text-block > :is(p, h2, h3)'},
        'format': '%B %d, %Y',
    },
    'https://amazonphotos.medium.com': {
        'news': 'article > div',
        'url': 'a[aria-label="Post Preview Title"]::attr(href)',
        'item': {},
        'details': {
            'title': ':is([class*=post-title], [class*=headline], h1)::text',
            'pub_date': '[class*=published-date] span::text',
            'text': '*:is(h1, [class*=post-body])',
        },
        'format': '%b %d, %Y',
    },
    'https://www.sync.com/blog': {
        'news': 'div.container:has(h3) div div:has(a)',
        'url': 'a::attr(href)',
        'item': {
            'title': 'strong::text',
        },
        'details': {
            'pub_date': (
                'div.container div[class*=col]:has(h1) > p:last-of-type::text'
            ),
            'text': 'div.blogpost > *',
        },
        'format': '%B %d, %Y',
    },
    'https://community.icedrive.net/c/release-logs/6': {
        'news': '.topic-list-item',
        'url': '.link-top-line a::attr(href)',
        'item': {'title': '.link-top-line a::text', 'summary': 'a.topic-excerpt'},
        'details': {
            'text': '.cooked > *',
            'pub_date': ':is(div.created-at, .post-date, .post-time)',
        },
        'pub_date_formatting': lambda x: re.sub(
            '[A-za-z]*', repl, re.search(r'\d{1,2} [A-Za-z]{3,9} \d{4}', x).group()
        ),
        'format': '%d %b %Y',
    },
    'https://blog.idrive.com': {
        'news': '.news-snippet',
        'url': '.news-title a::attr(href)',
        'item': {
            'title': '.news-title a::text',
            'pub_date': 'li:has(i.icon-calendar)::text',
        },
        'details': {'text': '.inner-article-content > *'},
        'format': '%B %d, %Y',
    },
    'https://media.mts.ru/news': {
        'news': '.category-block__holder div.category-block',
        'url': 'a[data-label=text_preview]::attr(href)',
        'item': {
            'title': 'a[data-label=text_preview]::text',
        },
        'details': {
            'pub_date': '[itemprop=datePublished]::attr(content)',
            'summary': '.article-block__subtitle',
            'text': '.article-block:not(:is(.article-block--appended)) .article-block__body-content > *:not(:is(:empty, div))',
        },
    },
    'https://sbercloud.ru/ru/warp/all': {
        'news': '[data-qa=warp-card]',
        'url': 'a::attr(href)',
        'item': {'title': 'h2::text', 'pub_date': '[data-qa=warp-card-date]::text'},
        'details': {
            'summary': (':is(.p-warp-article__desc, .c-constructor__hero-text)'),
            'text': ':is(.p-warp-article__block, [class*=content-desc]) > *',
        },
        'format': '%d %B %Y',
        'lang': 'ru_RU',
    },
    'https://blog.terabox.com': {
        'news': '#recent-content > [class*=post]',
        'url': '.entry-title a::attr(href)',
        'item': {
            'title': '.entry-title a::text',
            'summary': '.entry-summary',
            'pub_date': '.entry-date::text',
        },
        'details': {
            'text': ('.entry-content > *:not(:is(:empty, div, style, :has(img)))')
        },
        'format': '%d/%m/%Y',
    },
    'https://en-blog.timetreeapp.com': {
        'news': '#posts .post',
        'url': '.title a::attr(href)',
        'item': {
            'title': '.title a::text',
        },
        'details': {'pub_date': '.post-date::text', 'text': '.body-text > *'},
        'pub_date_formatting': lambda x: re.sub(r'[ndthrs]{1,2},', '', x),
        'format': '%b %d %Y',
    },
    'https://doodle.com/en/resources/blog': {
        'news': '[class*=GridContainer-module--cell] > div',
        'url': 'a::attr(href)',
        'item': {'title': 'h4::text', 'summary': 'p'},
        'details': {
            'text': '.Section-TextConstraint div[class*=ResourcesContainer]:has(h3) > *:not(:empty, div)',
            'pub_date': 'p[class*=author-department] span::text',
        },
        'pub_date_formatting': lambda x: x.split('Updated: '),
        'format': '%b %d, %Y',
    },
    'https://blog.teamup.com': {
        'news': '.recent-posts .post',
        'url': '.card-title a::attr(href)',
        'item': {'title': '.card-title a::text', 'summary': '.card-text'},
        'details': {
            'pub_date': ('meta[property="article:published_time"]::attr(content)'),
            'text': '.article-post > *',
        },
    },
    'https://www.teamup.com/news': {
        'news': '.lazyload-wrapper .table__row',
        'url': 'a::attr(href)',
        'item': {
            'title': 'a > span:first-of-type::text',
            'summary': '[data-key*=notes]',
            'pub_date': '[data-key=start]::text',
        },
        'details': {
            'text': '[class*=article__content] > *:not(:empty, figure)',
        },
        'format': '%d/%m/%Y',
    },
    'https://calendly.com/blog/category/whats-new': {
        'news': '#blog-articles-container a',
        'url': '::attr(href)',
        'item': {
            'title': '[direction=column] > p:first-of-type::text',
            'summary': '[direction=column] > div:first-of-type p::text',
        },
        'details': {
            'text': '[direction=column]:nth-child(2) > div > *:is(p, h2)',
            'pub_date': 'p:first-of-type:has(br)',
        },
        'pub_date_formatting': lambda x: re.search(r'<br>(.*)<\/p>', x)
        .group(1)
        .replace('.', ''),
        'format': '%b %d, %Y',
    },
    'https://www.usemotion.com/blog': {
        'news': '[class*=blog-cards] [role=listitem]',
        'url': 'a::attr(href)',
        'item': {
            'title': '.blog-card-title::text',
            'summary': '.blog-card_summary',
            'pub_date': '.blog-card_details > div:last-of-type::text',
        },
        'details': {'text': '#content > *:not(:is(:empty, div))'},
        'format': '%b %d, %Y',
    },
    'https://www.simplemobiletools.com/blog': {
        'news': '#articles .article-container',
        'url': 'a::attr(href)',
        'item': {
            'title': '.title-box h2::text',
            'pub_date': '.title-box time::attr(datetime)',
        },
        'details': {'text': 'article.text > p:has(span)'},
        'format': '%Y-%m-%d',
    },
    'https://ticktick.com/public/changelog/': {
        'news': 'body > script',
        'news_formatting': lambda x: ticktick_news_handler(x),
        'url': '',
        'item': {'h2::text'},
        'details': {
            'pub_date': 'h2::text',
            'text': 'li:not(:is(:has([class*=fixed]))) .detail-wrapper',
        },
        'format': '%Y-%m-%d',
    },
    'https://blog.doist.com': {
        'news': 'article.db-article-card',
        'url': '.db-article-card__title a::attr(href)',
        'item': {'title': '.db-article-card__title a::text', 'summary': 'p'},
        'details': {
            'pub_date': ('meta[property="article:published_time"]::attr(content)'),
            'text': '.db-article__body > :not(:is(:empty, figure, div))',
        },
    },
    'https://todoist.com/ru/help/articles/whats-new': {
        'news': '#__NEXT_DATA__',
        'news_formatting': lambda x: todoist_news_handler(x),
        'url': '',
        'item': {'script': lambda x: x},
    },
    'https://www.any.do/blog/announcements': {
        'news': 'article',
        'url': '.title a::attr(href)',
        'item': {
            'title': '.title a::text',
            'summary': '.post-excerpt',
        },
        'details': {
            'pub_date': ('meta[property="article:published_time"]::attr(content)'),
            'text': '.text > :not(:is(:empty, center))',
        },
    },
    'https://miro.com/blog/update': {
        'bs4': True,
        'broken_code': True,
        'news': '.article-item',
        'url': 'a',
        'item': {
            'title': 'a[class*=title]',
        },
        'details': {
            'pub_date': (['meta[property="article:published_time"]', 'content']),
            'summary': '.stk-post .stk-layout__overhangs_both div.stk-grid-col:not(:has(h1, h2, h3, h4, figure)) p:not(:empty)',
            'text': '.stk-post > .stk-grid:nth-child(1n+2) > div > *:not(figure, [class*=empty])',
        },
    },
    'https://blog.trello.com': {
        'news': '.bloglisting--post',
        'url': '::attr(href)',
        'item': {
            'title': '.bloglisting--post--title::text',
            'summary': '.bloglisting--post--description',
        },
        'details': {
            'pub_date': '[itemprop=datePublished]::text',
            'text': '#hs_cos_wrapper_post_body > *',
        },
        'format': '%B %d, %Y',
    },
    'https://coda.io/updates': {
        'news': '[data-coda-ui-id*=Group]:nth-child(1)',
        'url': '',
        'item': {'script': lambda x: coda_handler(x)},
    },
    'https://quip.com/blog': {
        'news': 'article.blog-article',
        'url': 'a::attr(href)',
        'item': {
            'title': '.title::text',
            'summary': '.snippet',
            'pub_date': '.time-delta::text',
        },
        'details': {
            'text': '.blog-post-detail > *:not(:is(h2, .author, figure))',
        },
        'format': '%B %d, %Y',
    },
    'https://www.craft.do/blog': {
        'news': 'section .grid > div',
        'url': 'a::attr(href)',
        'item': {'title': 'a div:nth-child(2)::text', 'summary': 'div:nth-child(3)'},
        'details': {
            'pub_date': 'section:first-of-type div p:nth-child(3)',
            'text': 'article > *:not(figure)',
        },
        'pub_date_formatting': lambda x: re.search(
            r'> *([A-Za-z]* \d{1,2}, \d{4}) *<\/p>', x
        ).group(1),
        'format': '%B %d, %Y',
    },
    'https://www.craft.do/whats-new': {
        'news': '[data-page-section=page-body]',
        'url': '',
        'item': {
            'title': 'h1::text',
            'text': '[data-page-section=page-body] > div:not([class])  > div > span > div > :not(a, :empty) :is(h1, h3, h4, p)',
            'pub_date': 'h1::text',
        },
        'pub_date_formatting': tz.now().strftime('%Y-%m-%d'),
        'format': '%Y-%m-%d',
    },
    'https://www.onlyoffice.com/blog/onlyoffice-in-the-press': {
        'news': 'article.post',
        'url': '.entry-title a::attr(href)',
        'item': {
            'title': '.entry-title a::text',
            'text': 'p',
            'pub_date': '.date::text',
        },
        'format': '%B %d, %Y',
    },
    'https://slite.com/blog-category/updates': {
        'news': '.blog-post-card:not([class*=invisible])',
        'url': 'a::attr(href)',
        'item': {
            'title': '.blog-post-card-title::text',
        },
        'details': {
            'pub_date': '.hero-blog-grid > div:first-of-type .label::text',
            'summary': '.hero-blog-title > .blog-post-subheader',
            'text': ('.section .blog-body-grid > div:first-of-type > *:not(figure)'),
        },
        'format': '%B %d, %Y',
    },
    'https://support.microsoft.com/en-us/office/what-s-new-in-microsoft': {
        'api_like': True,
        'news': '.content > *',
        'news_formatting': lambda x: support_microsoft_news_handler(x),
        'url': 'url',
        'item': {'pub_date': 'pub_date', 'title': 'title', 'text': 'text'},
    },
    'https://insider.office.com/ru-ru/blog': {
        'news': '.material-card',
        'url': '.link-group a::attr(href)',
        'item': {
            'title': '.card-body h3::text',
            'summary': '.card-body p:last-of-type',
            'pub_date': '.card-body .entry-date:first-of-type::text',
        },
        'details': {'text': '#content > *'},
        'format': '%b %d, %Y',
    },
    # HTTP code 403
    'https://polarisofficehelp.zendesk.com/hc/en-us/sections/4408785540239-Update-History': {
        'news': '.article-list-item',
        'url': 'a::attr(href)',
        'item': {},
        'details': {
            'title': '.article-title::text',
            'pub_date': '.meta-data:nth-child(2) time::attr(datetime)',
            'text': '.article-body > *',
        },
    },
    'https://www.wps.com/whatsnew/': {
        'news': 'article.article-content',
        'url': '',
        'item': {
            'title': '.article-title::text',
            'text': '.article-content-container > *',
            'pub_date': '.article-title::text',
        },
        'pub_date_formatting': lambda x: re.search(
            r'\d{1,2}\/\d{1,2}\/\d{4}', x
        ).group(),
        'format': '%m/%d/%Y',
    },
    'https://www.mobisystems.com/ru-ru/news': {
        'news': '.news-grid-item',
        'url': 'a::attr(href)',
        'item': {
            'title': '.news-item-title-wrap > h3::text',
            'summary': '.news-item-content-wrap',
            'pub_date': '.date-text::text',
        },
        'details': {
            'text': '.details-news-content-text > div > *',
        },
        'format': '%b %d, %Y',
    },
    'https://helpx.adobe.com/acrobat/using/whats-new': {
        'news': '#root_content_flex_items_position > .aem-Grid',
        'url': '',
        'item': {
            'title': '.cmp-text:has(.section-title) > h4::text',
            'text': ('div:nth-child(1n+4) *:is(h1, h2, h3, p, li):not(.callouts)'),
        },
        'root_pub_date': 'meta[name=lastModifiedDate]::attr(content)',
    },
    'https://www.notion.so/releases': {
        'news': 'article.release',
        'url': '.global-title a::attr(href)',
        'item': {
            'title': '.global-title a::text',
            'pub_date': 'time a::text',
            'text': 'article.rich-text > div > *',
        },
        'format': '%B %d, %Y',
    },
    'https://help.evernote.com/hc/en-us/articles/360058361833-Evernote': {
        'news': '.article-body > ul > li',
        'url': '',
        'item': {
            'title': 'h4::text',
            'pub_date': '.accordion_content em::text',
            'text': '.accordion_content > *',
        },
        'pub_date_formatting': lambda x: re.search(
            r'[A-Za-z]{3,9} \d{1,2}, \d{4}', x
        ).group(),
        'format': '%B %d, %Y',
    },
    'https://news.samsung.com/global/category/products/mobile': {
        'news': '.item > li',
        'url': 'a::attr(href)',
        'item': {'title': '.title::text', 'pub_date': '.date::text'},
        'details': {
            'text': '.text_cont > *',
        },
        'format': '%B %d, %Y',
    },
    'https://www.aboutamazon.com/news': {
        'news': '[data-content-type=article]',
        'url': '[class*=title] a::attr(href)',
        'item': {},
        'details': {
            'title': 'h1:is([class*=title], [class*=headline]) ::text',
            'pub_date': '[class*=datePublished]::attr(data-timestamp-iso)',
            'summary': 'article [class*=subHeadline]',
            'text': ('article [class*=ArticleBody-body] > :not(:is(div, :empty))'),
        },
    },
    'https://www.alibaba.com/blog/category/latest-news': {
        'news': '.post-content',
        'url': '.entry-title a::attr(href)',
        'item': {
            'title': '.entry-title a::text',
            'summary': '.entry-content > *:not(.read-more)',
            'pub_date': '[itemprop=datePublished]::text',
        },
        'details': {'text': '.entry-content > *:not(div)'},
        'format': '%B %d, %Y',
    },
    'https://ir.netease.com/news-releases': {
        'news': '.news-table tbody tr',
        'url': '[class*=headline] a::attr(href)',
        'item': {
            'title': '[class*=headline] a::text',
            'pub_date': '[class*=date-time]::text',
        },
        'details': {'text': '.xn-content > *'},
        'format': '%m/%d/%y',
    },
    'https://techcrunch.com': {
        'news': ':is(article, .feature-island-main-block)',
        'url': '[class*=title]:not([class*=event]) a::attr(href)',
        'item': {
            'title': '[class*=title]:not([class*=event]) a::text',
            'summary': '.post-block__content',
        },
        'details': {
            'pub_date': '[property="article:published_time"]::attr(content)',
            'text': '.article-content > *:not(:is(div, hr))',
        },
    },
    'https://vc.ru': {
        'news': '.feed__item',
        'url': '.content-link::attr(href)',
        'item': {
            'title': '.content-title::text',
            'summary': '.content-container > .l-island-a:not([class*=title])',
        },
        'details': {
            'pub_date': ('meta[property="article:published_time"]::attr(content)'),
            'text': '.content--full > *:not(:is(figure, .content-info))',
        },
    },
    'https://www.theverge.com': {
        'news': 'div:is([class*=content-card], [class*=content-block])',
        'url': 'a::attr(href)',
        'item': {},
        'details': {
            'title': 'h1::text',
            'pub_date': '[property="article:published_time"]::attr(content)',
            'summary': 'span:has(> h2) > h2',
            'text': '[class*=article-body-component] :is(h3, h4, p)',
        },
    },
    'https://www.washingtonpost.com/business/technology': {
        'bs4': True,
        'news': '.story-headline',
        'url': 'a[data-pb-local-content-field]',
        'item': {'title': '[class*=headline]', 'pub_date': '[data-qa=timestamp]'},
        'details': {
            'text': '.article-body > p',
        },
        'format': '%B %d, %Y',
    },
    'https://www.forbes.ru/tekhnologii': {
        'bs4': True,
        'news': 'main :has(> header, > a em)',
        'url': 'div > a:has(span, em, div)',
        'item': {
            'title': 'div > a:has(span, em, div) :is(span, em, div)',
            'summary': 'div > a:has(span, em, div) p',
        },
        'details': {
            'pub_date': ('time', 'datetime'),
            'text': '[data-article="0"] [itemprop=articleBody]',
        },
    },
    'https://www.bloomberg.com/technology': {
        'bs4': True,
        'news': ':is([class*=SingleStory], [class*=storyBlock])',
        'url': '[data-component=headline] a',
        'item': {
            'title': '[data-component=headline] a',
            'pub_date': ['time', 'datetime'],
        },
        'details': {
            'summary': '[class*=abstract-item-text]',
            'text': '.body-content > p',
        },
    },
    'https://www.kommersant.ru/hitech': {
        'bs4': True,
        'news': 'article.rubric_lenta__item',
        'url': 'h2 a',
        'item': {
            'title': 'h2 a',
        },
        'details': {
            'pub_date': ['time', 'datetime'],
            'text': 'article:has(.js-social) [itemprop=articleBody] > p',
        },
    },
    'https://www.wsj.com/news/technology': {
        'bs4': True,
        'news': 'article[class]',
        'url': '[class*=headline] a',
        'item': {'title': '[class*=headlineText]'},
        'details': {
            'pub_date': ['time', 'datetime'],
            'summary': '[class*=Dek]',
            'text': '[data-type=paragraph]',
        },
    },
    'https://www.ft.com/technology': {
        'bs4': True,
        'news': '.o-teaser__content',
        'url': 'a[class*=heading-link]',
        'item': {'title': 'a[class*=heading-link]', 'summary': 'p'},
        'details': {'pub_date': 'script[type="application/ld+json"]'},
        'pub_date_formatting': lambda x: json.loads(x)['datePublished'],
    },
    'https://www.vedomosti.ru/technologies': {
        'bs4': True,
        'news': '.grid-cell__body:has(time)',
        'url': 'a',
        'item': {
            'title': '[class*=_title]',
            'summary': '[class*=subtitle]',
            'pub_date': 'time',
        },
        'details': {
            'text': 'article:first-of-type .article-boxes-list__item:not(:empty)',
        },
        'format': '%d.%m.%Y',
    },
    'https://www.cnews.ru': {
        'news': '.mainnews_item',
        'url': '.mni-content a::attr(href)',
        'item': {'title': ' .mni-content p::text', 'pub_date': '.mnic-date::text'},
        'details': {
            'pub_date': '.article-date-mobile::text',
            'summary': '.lead',
            'text': ':is(.article_body, [class*=desc], .news_container) > *:not(:is(div, span))',
        },
        'pub_date_formatting': lambda x: re.sub(r' *\d{1,2}:\d{2}', '', x),
        'format': '%d %B %Y',
        'lang': 'ru_RU',
    },
    'https://habr.com/ru/news': {
        'news': 'article',
        'url': 'h2[class*=title] a::attr(href)',
        'item': {
            'title': 'h2[class*=title] a span::text',
            'pub_date': 'time::attr(datetime)',
        },
        'details': {
            'text': ('.article-formatted-body > div > *:not(:is(figure, :empty))'),
        },
    },
    'https://www.bigtechwire.com': {
        'news': '#tdi_91 .td-module-container',
        'url': '.entry-title a::attr(href)',
        'item': {'title': '.entry-title a::text', 'summary': '.td-excerpt'},
        'details': {
            'pub_date': '.td-post-title .entry-date::attr(datetime)',
            'text': '.td-post-content > *:not(:is(div, script))',
        },
    },
    'https://www.producthunt.com/topics/': {
        'news': 'ul > div',
        'url': 'a::attr(href)',
        'item': {
            'title': 'div > a > div:nth-child(1)::text',
            'summary': 'div > a > div:nth-child(2)::text',
        },
        'details': {
            'pub_date': 'script[type="application/ld+json"]::text',
            'text': 'main[class*=layout] > div > div > div.direction-column:nth-child(2) > div',
        },
        'pub_date_formatting': lambda x: json.loads(x)[0]['datePublished'],
    },
    # COMMENT: тут начинается RUSTORE
    'https://support.google.com/product-documentation/answer/11412553': {
        'api_like': True,
        'news': '.article-content-container .cc > *',
        'news_formatting': lambda x: support_google_news_handler(x),
        'url': '',
        'item': {'pub_date': 'pub_date', 'title': 'title', 'text': 'text'},
    },
    'https://www.androidpolice.com': {
        'news': '.section-latest-news .article',
        'url': '.display-card-title a::attr(href)',
        'item': {
            'title': '.display-card-title a::text',
        },
        'details': {
            'pub_date': '.heading_meta time::attr(datetime)',
            'summary': '.heading_excerpt',
            'text': '[class*=content-block] > *:not(:is(div, script))',
        },
    },
    'https://www.xda-developers.com': {
        'news': '.section-latest-news .article',
        'url': '[class*=card-content] h5 a::attr(href)',
        'item': {
            'title': '[class*=card-content] h5 a::text',
            'summary': '[class*=excerpt]',
            'pub_date': 'time::attr(datetime)',
        },
        'details': {
            'text': '[class*=content-block] > *:not(div)',
        },
    },
    'https://www.sammobile.com': {
        'news': 'div:is(.tns-item[class*=active], .articles) > div:is([class*="article-item article-item"], .article-item)',
        'url': 'a::attr(href)',
        'item': {'title': 'h4.line-clamp::text', 'summary': 'p.line-clamp'},
        'details': {
            'pub_date': '[itemprop=datePublished]::attr(content)',
            'text': '[itemprop=articleBody] > *:not(div)',
        },
    },
    'https://www.sammyfans.com': {
        'news': '.mvp-blog-story-wrap',
        'url': 'a::attr(href)',
        'item': {
            'title': 'h2::text',
        },
        'details': {
            'pub_date': '[itemprop=datePublished]::attr(datetime)',
            'text': '#mvp-content-main > *',
        },
        'format': '%Y-%m-%d',
    },
    'https://www.huawei.ru/news': {
        'news': '.news-item',
        'url': '*::attr(href)',
        'item': {
            'title': '.news-item__title::text',
            'pub_date': '.news-item__date::text',
        },
        'details': {
            'text': '.main .text > *',
        },
        'format': '%d.%m.%Y',
    },
    'https://www.huaweicentral.com': {
        'news': '.mvp-blog-story-col',
        'url': 'a::attr(href)',
        'item': {
            'title': 'h2::text',
        },
        'details': {
            'pub_date': '[itemprop=datePublished]::attr(datetime)',
            'text': '#mvp-content-main > *',
        },
        'format': '%Y-%m-%d',
    },
    'https://go.buy.mi.com': {
        'api': True,
        'news': 'data',
        'news_formatting': lambda x: x['page_data'],
        'url': 'assembly_info',
        'url_formatting': lambda x: x[0]['go_to_url'],
        'item': {'script': lambda x: mi_handler(x)},
    },
    'https://vk.com/': {
        'news': '.wall_posts .wall_item',
        'url': '.wi_date::attr(href)',
        'item': {
            'pub_date': '.wi_date::text',
        },
        'details': {
            'text': '.pi_text',
        },
        'pub_date_formatting': lambda x: text_date(x.replace('\xa0', ' ')),
        'format': '%d %b %Y',
    },
    'https://www.gazeta.ru': {
        'news': ':is([class*=w_col], .b_newslist) > a:has(*)',
        'url': '*::attr(href)',
        'item': {
            'title': '[class*=title]::text',
        },
        'details': {
            'pub_date': 'article time::attr(datetime)',
            'summary': '[itemprop=description]',
            'text': '#_id_main_article [class*=article-text] > *',
        },
    },
    'https://developer.apple.com/news': {
        'news': 'article[id]',
        'url': '.article-title::attr(href)',
        'item': {
            'title': '.article-title h2::text',
            'pub_date': '.article-date::text',
            'text': '.article-text > *',
        },
        'format': '%B %d, %Y',
    },
    'https://digiato.com/': {
        'news': '#todaysNews .rowCard',
        'url': '.rowCard__title::attr(href)',
        'item': {'title': '.rowCard__title::text', 'summary': 'rowCard__description'},
        'details': {
            'pub_date': '[property="article:modified_time"]::attr(content)',
            'text': ':is(.articlePost, .content) > *:not(:is(div, figure, script))',
        },
        'translate': True,
    },
    'https://medium.com/': {
        'news': 'div[data-post-id]',
        'url': 'a[data-post-id]::attr(href)',
        'item': {'title': 'h3 div::text', 'summary': 'a div div::text'},
        'details': {
            'pub_date': ('meta[property="article:published_time"]::attr(content)'),
            'text': '*:is(h1, [class*=post-body])',
        },
    },
    'https://newsblog.cafebazaar.ir': {
        'bs4': True,
        'news': '.post-grids-item',
        'url': '.post-grids-info-content',
        'item': {'title': '.post-grids--title', 'summary': '.post-grids--summary'},
        'details': {
            'pub_date': ['[property="article:published_time"]', 'content'],
            'text': '.post-body > *:not(figure)',
        },
        'format': '%Y-%m-%d %H:%M:%S',
        'translate': True,
    },
    'https://36kr.com/information/web_news': {
        'news': '.kr-flow-article-item',
        'url': '.article-item-title::attr(href)',
        'item': {
            'title': '.article-item-title::text',
            'summary': '.article-item-description',
        },
        'details': {
            'pub_date': '.item-time::text',
            'text': '.articleDetailContent > *:is(:not([class*=image], [class*=img]))',
        },
        'format': '%Y-%m-%d %H:%M',
    },
    'http://sj.360.cn/changelog': {
        'news': ':is(.changelogs, li:has(.detail))',
        'url': '',
        'item': {
            'title': 'h2::text',
            'pub_date': 'h2 span::text',
            'text': ':is(ol, .detail) > *:not(em)',
        },
        'format': '%Y-%m-%d',
        'translate': True,
    },
    'https://www.onestorecorp.com/en/news/newslink': {
        'news': 'table.table:nth-of-type(2) tr',
        'url': '*::attr(onclick)',
        'url_formatting': lambda x: x.split('location.href=')[-1].strip("'"),
        'item': {'title': 'p::text', 'text': 'p::text', 'pub_date': '*'},
        'pub_date_formatting': lambda x: re.search(
            r'</p> *(\d{4}-\d{2}-\d{2})</td>', x
        ).group(1),
        'format': '%Y-%m-%d',
        'translate': True,
    },
    'https://news.mt.co.kr/newsList': {
        'news': '#content li.bundle',
        'url': '.subject a::attr(href)',
        'item': {'title': '.subject a::text', 'summary': '.txt a'},
        'details': {'pub_date': '.date::text', 'text': '#textBody'},
        'format': '%Y.%m.%d %H:%M',
        'translate': True,
    },
    'https://app-time.ru/news': {
        'news': '.module[class*=lenta] .item-grid',
        'url': '.link::attr(href)',
        'item': {'title': 'h2::text', 'pub_date': '.date::text'},
        'details': {'text': '.wrap-inner-post > *:not(div)'},
        'pub_date_formatting': lambda x: text_date(x, fmt='%d %B %Y'),
        'format': '%d %B %Y',
    },
    'https://news.samsung.com/ru/latest': {
        'news': '.board_news li',
        'url': 'a::attr(href)',
        'item': {'title': '.title::text', 'pub_date': '.date::text'},
        'details': {
            'text': '.text_cont > *',
        },
        'format': '%d-%m-%Y',
    },
    'https://xiaomiui.net/miui': {
        'news': 'article.post',
        'url': 'a::attr(href)',
        'item': {
            'title': '.entry-title::text',
            'summary': '.excerpt',
            'pub_date': '.thb-post-date::attr(title)',
        },
        'details': {'text': '.entry-content > *:is(p, h2):not(:empty)'},
    },
    'https://www.honor.ru/club/forumplate/forumid-3': {
        'news': '.plate-comments-mob .plate-comment',
        'url': '.plate-comment-pre a::attr(href)',
        'item': {
            'title': '.plate-comment-pre a span::text',
            'pub_date': '.plate-comment-next .plate-::text',
        },
        'details': {
            'text': '.last_comment_content_info_wap > *:not(br)',
        },
        'pub_date_formatting': lambda x: (
            (dt.datetime.fromtimestamp(int(x) / 1000).strftime('%d-%m-%Y %H:%M:%S'))
            if re.search(r'\d{13}', x)
            else x
        ),
        'format': '%d-%m-%Y %H:%M:%S',
    },
    'https://www.ixbt.com/news': {
        'news': '.item',
        'url': 'a:has(strong)::attr(href)',
        'item': {},
        'details': {
            'title': '#newsheader::text',
            'pub_date': '[itemprop=datePublished]::attr(content)',
            'text': '#main-pagecontent__div > p',
        },
        'format': '%Y-%m-%d',
    },
    'https://www.sony.ru/presscentre/news': {
        'news': '[class*=news-list] > div [class*=content]',
        'url': 'a::attr(href)',
        'item': {
            'title': 'a::text',
            'summary': '[class*=desc]',
            'pub_date': '[class*=date] span::text',
        },
        'details': {
            'text': 'div[class*=desc] div[class*=desc] > *',
        },
        'pub_date_formatting': lambda x: re.sub(r'[^\s\d]*\.,', repl, x),
        'format': '%d %B %Y',
        'lang': 'ru_RU',
    },
    'https://4pda.to': {
        'news': 'article[class*=post]:has(h2)',
        'url': '.list-post-title a::attr(href)',
        'item': {
            'title': '.list-post-title span::text',
            'summary': '[itemprop=description]',
            'pub_date': '.date::text',
        },
        'details': {
            'text': '[itemprop=articleBody] > *:not(meta):not(div)',
        },
        'format': '%d.%m.%y',
    },
    'https://www.rbc.ru': {
        'news': '.item__wrap',
        'url': 'a::attr(href)',
        'item': {
            'title': '.item__title::text',
        },
        'details': {
            'pub_date': '[itemprop=datePublished]::attr(datetime)',
            'text': '[itemprop=articleBody] > *:not(div)',
        },
    },
    'https://rozetked.me/news': {
        'news': '.post_new',
        'url': '.post_new-title a::attr(href)',
        'item': {
            'title': '.post_new-title::text',
        },
        'details': {
            'pub_date': '[class*=meta-author] [class*=created]::text',
            'text': '#news-data > :not(div)',
        },
        'pub_date_formatting': lambda x: text_date(x),
    },
    'https://www.developer-tech.com/': {
        'news': 'article',
        'url': '.article-header a::attr(href)',
        'item': {'title': '.article-header a::attr(title)', 'summary': '.post-text'},
        'details': {
            'text': '.entry-content .cell > p',
            'pub_date': '[property="article:published_time"]::attr(content)',
        },
    },
    'https://dtf.ru/': {
        'news': '.feed .feed__item',
        'url': '.content-link::attr(href)',
        'item': {'title': '.content-title::text', 'pub_date': '.time::attr(title)'},
        'details': {
            'text': '.content--full > .l-island-a:not(.content-info)',
        },
        'pub_date_formatting': lambda x: re.search(r'\d{1,2}.\d{1,2}.\d{4}', x).group(),
        'format': '%d.%m.%Y',
    },
}
