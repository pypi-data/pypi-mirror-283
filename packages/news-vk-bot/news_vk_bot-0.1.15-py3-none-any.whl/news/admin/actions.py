from django.contrib.admin import action
from django.utils.translation import gettext_lazy as _

from news.handlers.dispatcher import send_admin_message_dispatch
from news.models import BotUser


@action(description='Отправить сообщения всем пользователям')
def send_admin_message(modeladmin, request, queryset):
    send_admin_message_dispatch(queryset)


@action(description=_('Пометить выбранные новости, прошедшими модерацию'))
def moderate_all(modeladmin, request, queryset):
    queryset.update(is_moderated=True)


@action(description=_('Пометить выбранные новости новыми (не прошедшими модерацию)'))
def new_all(modeladmin, request, queryset):
    queryset.update(is_moderated=False)


@action(description=_('Убрать выбранные новости из черного списка'))
def remove_all_from_blacklist(modeladmin, request, queryset):
    queryset.update(is_blacklisted=True)


@action(description=_('Добавить выбранные новости в черный список'))
def blacklist_all(modeladmin, request, queryset):
    queryset.update(is_blacklisted=False)


@action(description=_('Удалить выбранные новости'))
def delete_all(modeladmin, request, queryset):
    queryset.filter(address__for_parser=False).delete()
    queryset.update(is_deleted=True)


@action(description=_('Перенести из отправленных в прошедшие модерацию'))
def unsend_all(modeladmin, request, queryset):
    for user in BotUser.objects.all():
        for news_item in queryset:
            user.received_news.remove(news_item)
