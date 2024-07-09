from scrapy_djangoitem import DjangoItem

from news.models import News


class NewsItem(DjangoItem):
    django_model = News
