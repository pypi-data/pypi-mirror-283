from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NewsParsingConfig(AppConfig):
    name = 'news_parsing'
    verbose_name = _('Данные о состоянии сбора новостей')
