from os import getenv

from django.contrib import admin
from django.utils import timezone as tz
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from rangefilter.filter import DateRangeFilter

from news_bot.settings import EMPTY_ADMIN_VALUE, NEWS_DAYS

from ..models import (Address, AdminMessage, BotUser, KeyWord, News, Reaction,
                      Service, Stream)
from .actions import (blacklist_all, delete_all, moderate_all, new_all,
                      remove_all_from_blacklist, send_admin_message,
                      unsend_all)
from .filters import (BlackListFilter, ModeratedNewsFilter,
                      ServiceInStreamFilter, SourcesFilter, SourceTypeFilter,
                      StreamInCompanyFilter)
from .forms import NewsAdminForm, NewsCreationForm

load_dotenv()


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    add_form = NewsCreationForm
    list_display = (
        'stream',
        'view_service',
        'pub_date',
        'title',
        'text_preview',
        'external_url',
    )
    list_display_links = ('title', 'text_preview')
    empty_value_display = EMPTY_ADMIN_VALUE
    search_fields = ('title', 'summary', 'text', 'address__address')
    list_filter = (
        ModeratedNewsFilter,
        BlackListFilter,
        ('pub_date', DateRangeFilter),
        'stream__company',
        SourceTypeFilter,
        StreamInCompanyFilter,
        ServiceInStreamFilter,
        SourcesFilter,
    )
    actions = [
        moderate_all,
        new_all,
        unsend_all,
        blacklist_all,
        remove_all_from_blacklist,
        delete_all,
    ]

    @admin.display(description=_('Ссылка на новость'))
    def external_url(self, obj):
        return format_html(f'<a href="{obj.url}">{obj.url}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_deleted=False)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_rangefilter_pub_date_default(self, request):
        return (
            tz.now().date() - tz.timedelta(days=tz.now().weekday()),
            tz.now().date(),
        )

    @admin.display(description=_('Сервис'))
    def view_service(self, obj):
        return obj.address.service.name

    @admin.display(description=_('Предпросмотр новости'))
    def text_preview(self, obj):
        if obj.text and obj.text.strip():
            return obj.text[:100] + '...' * (len(obj.text) > 100)
        return EMPTY_ADMIN_VALUE

    # @admin.display(description=_('Краткое описание'))
    # def desc_preview(self, obj):
    #     if obj.summary and obj.summary.strip():
    #         return obj.summary[:100] + '...' * (len(obj.summary) > 100)
    #     return EMPTY_ADMIN_VALUE

    def has_delete_permission(self, request, obj=None):
        if obj and not obj.address.for_parser:
            return True
        return False


@admin.register(AdminMessage)
class AdminMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'message')
    list_display_links = ('message',)

    actions = (send_admin_message,)


@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'kw_type')
    list_editable = ('name', 'kw_type')
    list_filter = ('kw_type',)
    search_fields = ('name',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'address',
        'service',
        # 'search_key_words',
        # 'search_add_key_words',
    )
    list_editable = (
        'address',
        'service',
        # 'search_key_words',
        # 'search_add_key_words',
    )
    list_filter = (
        'service__stream',
        ServiceInStreamFilter,
        # 'search_key_words',
        # 'search_add_key_words',
    )
    search_fields = ('address',)
    empty_value_display = EMPTY_ADMIN_VALUE

    def get_queryset(self, request):
        return super().get_queryset(request).filter(for_parser=True)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'stream', 'view_key_words', 'view_sources')
    search_fields = ('name', 'stream__name', 'key_words__name')
    list_filter = ('stream', SourcesFilter)
    empty_value_display = EMPTY_ADMIN_VALUE

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(name='Не определен')

    @admin.display(description=_('Ключевые слова'))
    def view_key_words(self, obj):
        return ', '.join(
            [
                (
                    '+' * (key_word.kw_type == 'add_key_word')
                    + '-' * (key_word.kw_type == 'blacklist')
                    + key_word.name
                )
                for key_word in obj.key_words.all()
            ]
        )

    @admin.display(description=_('Источники'))
    def view_sources(self, obj):
        return format_html(
            '<br>'.join(
                [
                    f'<a href="{url.address}">{url.address}</a>'
                    for url in (Address.objects.filter(service=obj))
                ]
            )
        )


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_editable = (
        'name',
        'is_active',
    )
    search_fields = ('name',)
    empty_value_display = EMPTY_ADMIN_VALUE

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(name='Не определен')


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    # filter_horizontal = ('streams',)
    list_display = ('user_id', 'is_superuser', 'weekday', 'receiving_time')
    list_editable = ('is_superuser', 'weekday', 'receiving_time')
    # list_display_links = ('user_id',)
    list_display_links = None
    list_filter = ('is_superuser',)
    search_fields = ('user_id',)


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = (
        'monday_date',
        'get_monday_date_likes',
        'get_monday_date_dislikes',
        'get_monday_date_no_reaction',
    )
    list_display_links = None

    def get_queryset(self, request):
        qs = super().get_queryset(request).distinct('monday_date')
        if getenv('STAT_NEW', default=False):
            return qs.filter(
                monday_date__lte=tz.now().date() - tz.timedelta(days=NEWS_DAYS)
            )
        return qs
