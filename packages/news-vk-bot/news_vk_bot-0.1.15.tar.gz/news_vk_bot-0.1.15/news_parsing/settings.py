import os
import sys

import django

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..")
)
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_bot.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = 'true'
django.setup()

BOT_NAME = "news_parsing"

SPIDER_MODULES = ["news_parsing.spiders"]
NEWSPIDER_MODULE = "news_parsing.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "news_parsing.pipelines.NewsParsingPipeline": 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOAD_FAIL_ON_DATALOSS = False

LOG_LEVEL = 'WARNING'
LOG_FILE = 'err.log'
