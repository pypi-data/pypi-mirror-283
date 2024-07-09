from django.db import models
from django.utils.translation import ugettext_lazy as _


class Parsing(models.Model):
    last_start = models.DateTimeField(_('Дата и время начала парсинга'))
    last_end = models.DateTimeField(_('Дата и время окончания парсинга'))
    last_log_renewal = models.DateField(_('Дата последнего обновления лог-файла'))
    sent = models.BooleanField(_('Информация отправлена'), default=False)

    class Meta:
        verbose_name = _('Парсинг')
        verbose_name_plural = _('Парсинг')
