from urllib.parse import urlparse

from django.contrib import admin
from django.core.exceptions import FieldError
from django.db.models import F, Q
from django.utils import timezone as tz
from django.utils.translation import gettext_lazy as _

from ..models import Address, BotUser, Service, Stream


class PubDateFilter(admin.SimpleListFilter):
    title = _('Дата публикации')
    parameter_name = 'pub-date'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Сегодня')),
            ('this_week', _('На этой неделе')),
            ('this_month', _('В этом месяце')),
            ('old', _('Старые')),
            ('all', _('Все')),
        )

    def queryset(self, request, queryset):
        now = tz.now().date()
        if self.value() == 'today':
            return queryset.filter(pub_date=now)
        if self.value() == 'this_month':
            return queryset.filter(pub_date__gt=now - tz.timedelta(days=now.day))
        if self.value() == 'old':
            return queryset.filter(pub_date__lte=now - tz.timedelta(days=now.day))
        if self.value() == 'all':
            return queryset
        return queryset.filter(pub_date__gte=now - tz.timedelta(days=now.weekday()))

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            if str(lookup) == 'this_week':
                yield {
                    'selected': self.value() == str(lookup) or (self.value() is None),
                    'query_string': changelist.get_query_string(
                        remove=[self.parameter_name]
                    ),
                    'display': title,
                }
            else:
                yield {
                    'selected': self.value() == str(lookup),
                    'query_string': changelist.get_query_string(
                        {self.parameter_name: lookup}
                    ),
                    'display': title,
                }


class BlackListFilter(admin.SimpleListFilter):
    title = _('Поиск по ключевым словам')
    parameter_name = 'is_blacklisted'

    def lookups(self, request, model_admin):
        return (
            ('no', _('Основной список')),
            ('yes', _('Попали в стоп-лист')),
            ('all', _('Все')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_blacklisted=True)
        if self.value() == 'all':
            return queryset
        return queryset.filter(is_blacklisted=False)

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            if str(lookup) == 'no':
                yield {
                    'selected': self.value() == str(lookup) or (self.value() is None),
                    'query_string': changelist.get_query_string(
                        remove=[self.parameter_name]
                    ),
                    'display': title,
                }
            else:
                yield {
                    'selected': self.value() == str(lookup),
                    'query_string': changelist.get_query_string(
                        {self.parameter_name: lookup}
                    ),
                    'display': title,
                }


class StreamInCompanyFilter(admin.SimpleListFilter):
    title = _('Стримы компании')
    parameter_name = 'stream'
    related_filter_parameter = 'stream__company__exact'

    def lookups(self, request, model_admin):
        streams = []
        queryset = Stream.objects.all()
        if self.related_filter_parameter in request.GET:
            queryset = queryset.filter(
                company=request.GET[self.related_filter_parameter]
            )
        for stream in queryset:
            streams.append((str(stream.id), stream.name))
        return sorted(streams, key=lambda x: x[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(stream_id=self.value())
        return queryset


class ServiceInStreamFilter(admin.SimpleListFilter):
    title = _('Сервисы стрима')
    parameter_name = 'service'
    related_filter_parameter = [
        'service__stream__id__exact',
        'stream__id__exact',
        'stream',
    ]
    company_filter_parameter = 'stream__company__exact'

    def lookups(self, request, model_admin):
        services = []
        queryset = Service.objects.all()
        for rel_param in self.related_filter_parameter:
            if rel_param in request.GET:
                queryset = queryset.filter(stream_id=request.GET[rel_param])
        if self.company_filter_parameter in request.GET:
            queryset = queryset.filter(
                stream__in=Stream.objects.filter(
                    company=request.GET[self.company_filter_parameter]
                )
            )
        for service in queryset:
            services.append((str(service.id), service.name))
        return sorted(services, key=lambda x: x[1])

    def queryset(self, request, queryset):
        if self.value():
            try:
                return queryset.filter(service_id=self.value())
            except FieldError:
                return queryset.filter(address__service_id=self.value())
        return queryset


class SourceTypeFilter(admin.SimpleListFilter):
    title = _('Тип источника')
    parameter_name = 'source_type'
    related_name_parameter = 'stream__company__exact'

    def lookups(self, request, model_admin):
        if self.related_name_parameter in request.GET and (
            request.GET[self.related_name_parameter] == 'mailru'
        ):
            return (
                ('service_blogs', _('Блоги сервисов')),
                ('appstore', _('AppStore')),
                ('data_ai', _('data.ai')),
                ('net_sources', _('Интернет-издания')),
            )
        return None

    def queryset(self, request, queryset):
        if self.related_name_parameter in request.GET:
            if self.value() == 'appstore':
                return queryset.filter(address__address__contains='apps.apple.com')
            if self.value() == 'data_ai':
                return queryset.filter(address__address__contains='data.ai')
            if self.value() == 'net_sources':
                return queryset.filter(
                    address__search_key_words=True, address__search_add_key_words=False
                )
            if self.value() == 'service_blogs':
                return queryset.filter(
                    ~Q(address__address__contains='apps.apple.com')
                    & ~Q(address__address__contains='data.ai'),
                    address__search_key_words=F('address__search_add_key_words'),
                )
        return queryset


class ModeratedNewsFilter(admin.SimpleListFilter):
    title = _('Модерация')
    parameter_name = 'is_moderated'

    def lookups(self, request, model_admin):
        return (
            ('new', _('Новые новости (нужна модерация)')),
            ('moderated', _('Прошли модерацию, но пока не отправлены')),
            ('sent', _('Отправлены пользователям')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'new':
            return queryset.filter(is_moderated=False)
        sent_messages = set(
            BotUser.objects.filter(is_active=True).values_list(
                'received_news', flat=True
            )
        )
        if self.value() == 'moderated':
            return queryset.filter(~Q(id__in=sent_messages), is_moderated=True)
        if self.value() == 'sent':
            return queryset.filter(id__in=sent_messages)
        return queryset


class SourcesFilter(admin.SimpleListFilter):
    title = _('Источники')
    parameter_name = 'source'
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        queryset = set()
        for addr in Address.objects.all().values_list('address', flat=True):
            url = urlparse(addr).netloc
            if url.startswith('www.'):
                url = url[4:]
            queryset.add((url, url))
        return sorted(queryset, key=lambda x: x[1])

    def queryset(self, request, queryset):
        if self.value():
            try:
                return queryset.filter(address__address__contains=self.value())
            except FieldError:
                services = Address.objects.filter(
                    address__contains=self.value()
                ).values_list('service', flat=True)
                return queryset.filter(id__in=list(services))
        return queryset
