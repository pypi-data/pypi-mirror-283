import json
import logging
from os import getenv

import numpy as np
import schedule
from django.db.models import Q
from django.utils import timezone as tz
from dotenv import load_dotenv

from monitoring.constants import DEFAULT_TIME_TO_SEND, TIME_TO_GATHER_METRIC
from monitoring.metrics import (
    ALL_USERS_ADMIN_NOTIFICATION, NUMBER_OF_DISLIKES,
    NUMBER_OF_ERRORS_IN_ALL_USERS_ADMIN_NOTIFICATION,
    NUMBER_OF_ERRORS_IN_SENDER, NUMBER_OF_LIKES, NUMBER_OF_NO_NEWS,
    SENT_EVERYDAY, SENT_MESSAGES, SENT_ON_MONDAY, TIME_TO_SEND_A_MESSAGE,
    get_current_number_of_news, get_current_number_of_users)
from news.handlers.messages import (CHOOSE_TIME, CORRECT_EVERYDAY,
                                    CORRECT_MONDAY, CORRECT_STREAMS,
                                    CORRECT_TIME, END_STREAMS, FIRST_START,
                                    HELP, HELP_TEXT, HOUR, MINUTES, NO_NEWS,
                                    NO_STREAMS, NO_TIME, REACTION_ANSWER,
                                    REPEAT_START, STREAMS_HELP, TIME_START,
                                    WEEKDAY_HELP, WEEKDAY_INLINE,
                                    WEEKDAY_OPTIONS, news_post)
from news.models import BotUser, News, Reaction, Stream, get_defined
from news_bot.settings import DELETE_NEWS_AFTER_DAYS, NEWS_DAYS

load_dotenv()

CHECKED = ' \u2714'
FORMAT = '%d-%m-%Y'


def set_schedule(bot, user):
    schedule.clear(str(user.user_id))
    try:

        # schedule.every(1).minutes.do(send_news, bot=bot, user=user).tag(
        #     str(user.user_id), user.weekday
        # )

        schedule.every(1).weeks.do(delete_dangling_news)

        schedule.every().day.at(
            TIME_TO_GATHER_METRIC, getenv('TZ', default='Europe/Moscow')
        ).do(get_current_number_of_news)

        schedule.every().day.at(
            TIME_TO_GATHER_METRIC, getenv('TZ', default='Europe/Moscow')
        ).do(get_current_number_of_users)

        time_to_send_message = user.receiving_time
        if not time_to_send_message:
            time_to_send_message = DEFAULT_TIME_TO_SEND
        if user.weekday == 'every':
            SENT_EVERYDAY.inc()
            schedule.every().day.at(
                time_to_send_message, getenv('TZ', default='Europe/Moscow')
            ).do(send_news, bot=bot, user=user).tag(str(user.user_id), user.weekday)
        else:
            SENT_ON_MONDAY.inc()
            schedule.every().monday.at(
                time_to_send_message, getenv('TZ', default='Europe/Moscow')
            ).do(send_news, bot=bot, user=user).tag(str(user.user_id), user.weekday)
    except TypeError as exc:
        logging.error(f'Error during schedule {exc}')
        schedule.every().monday.at(
            '12:00:00', getenv('TZ', default='Europe/Moscow')
        ).do(send_news, bot=bot, user=user).tag(str(user.user_id), user.weekday)


def delete_dangling_news():
    try:
        News.objects.filter(
            Q(is_deleted=True)
            | Q(pub_date__lt=tz.now() - tz.timedelta(days=DELETE_NEWS_AFTER_DAYS))
        ).delete()
    except Exception as e:
        logging.error(f'Error during news deletion: {e}')


@ALL_USERS_ADMIN_NOTIFICATION.track_inprogress()
@NUMBER_OF_ERRORS_IN_ALL_USERS_ADMIN_NOTIFICATION.count_exceptions()
def notify_every_user(bot, queryset):
    for user in BotUser.objects.all():
        for admin_message in queryset:
            sender(bot, chat_id=user.user_id, separate_message=admin_message)


def get_user_id(event):
    if event.data.get('from'):
        return event.data['from']['userId']
    if event.data.get('chat'):
        return event.data['chat']['chatId']
    return event.data['message']['chat']['chatId']


@TIME_TO_SEND_A_MESSAGE.time()
@NUMBER_OF_ERRORS_IN_SENDER.count_exceptions()
def sender(
    bot,
    chat_id=None,
    query_id=None,
    markup=None,
    msg_id=None,
    message='',
    text='',
    alert=False,
    url='',
    separate_message='',
):
    if msg_id:
        if markup:
            bot.edit_text(
                chat_id=chat_id,
                msg_id=msg_id,
                text=message,
                inline_keyboard_markup=json.dumps(markup),
            )
        else:
            bot.edit_text(chat_id=chat_id, msg_id=msg_id, text=message)
    else:
        if separate_message:
            bot.send_text(chat_id=chat_id, text=separate_message)
        if markup:
            bot.send_text(
                chat_id=chat_id, text=message, inline_keyboard_markup=json.dumps(markup)
            )
    if query_id:
        bot.answer_callback_query(
            query_id=query_id, text=text, show_alert=alert, url=url
        )
    SENT_MESSAGES.inc()


def send_news(bot, user):
    if not user.get_stream_names():
        bot.send_text(chat_id=user.user_id, text=NO_STREAMS)
    else:
        news = News.objects.filter(
            stream__name__in=user.get_stream_names(),
            pub_date__gte=tz.now() - tz.timedelta(days=NEWS_DAYS),
            is_moderated=True,
            is_deleted=False,
        ).exclude(id__in=list(user.received_news.all().values_list('id', flat=True)))
        if not news:
            NUMBER_OF_NO_NEWS.inc()
            sender(bot, chat_id=user.user_id, separate_message=NO_NEWS)
        else:
            monday_date = tz.now().date()
            text = news_post(news)
            try:
                reaction, _ = Reaction.objects.get_or_create(
                    monday_date=monday_date, user=user
                )
                reaction.news_temp = text
                reaction.save()
                reaction_inline = json.dumps(
                    [
                        [
                            {
                                'text': '\U0001F44D',
                                'callbackData': f'like_{reaction.pk}',
                            },
                            {
                                'text': '\U0001F44E',
                                'callbackData': f'dislike_{reaction.pk}',
                            },
                        ]
                    ]
                )
                bot.send_text(
                    chat_id=user.user_id,
                    text=text,
                    parse_mode='HTML',
                    inline_keyboard_markup=reaction_inline,
                )
                user.received_news.add(*list(news.values_list('id', flat=True)))
                user.save()
                SENT_MESSAGES.inc()
            except Exception as e:
                logging.error(f'Error during sending news: {e}')


def like_cb(bot, event):
    user_id = get_user_id(event)
    like, pk = event.data['callbackData'].split('_')
    reaction = Reaction.objects.get(pk=pk)
    reaction.reaction = like
    reaction.save()
    bot.edit_text(
        chat_id=user_id,
        msg_id=event.data['message']['msgId'],
        text=reaction.news_temp,
        parse_mode='HTML',
    )
    NUMBER_OF_LIKES.inc()
    sender(
        bot,
        chat_id=user_id,
        query_id=event.data['queryId'],
        separate_message=REACTION_ANSWER,
    )


def dislike_cb(bot, event):
    user_id = get_user_id(event)
    dislike, pk = event.data['callbackData'].split('_')
    reaction = Reaction.objects.get(pk=pk)
    reaction.reaction = dislike
    reaction.save()
    bot.edit_text(
        chat_id=user_id,
        msg_id=event.data['message']['msgId'],
        text=reaction.news_temp,
        parse_mode='HTML',
    )
    NUMBER_OF_DISLIKES.inc()
    sender(
        bot,
        chat_id=user_id,
        query_id=event.data['queryId'],
        separate_message=REACTION_ANSWER,
    )


def help_cb(bot, event):
    user_id = get_user_id(event)
    user, _ = BotUser.objects.get_or_create(user_id=user_id)
    help_markup = HELP.copy()
    if user.is_superuser is True:
        help_markup.append(WEEKDAY_OPTIONS)
    sender(bot, chat_id=user_id, message=HELP_TEXT, markup=help_markup)


def weekday_cb(bot, event):
    wd_names = {'every': 'каждый день', 'monday': 'понедельник'}
    cb = event.data["callbackData"]
    user_id = get_user_id(event)
    user, _ = BotUser.objects.get_or_create(user_id=user_id)
    if cb == 'weekday_cb':
        if not user.receiving_time:
            sender(
                bot,
                chat_id=user_id,
                query_id=event.data['queryId'],
                text=CHOOSE_TIME,
                alert=True,
            )
        else:
            sender(
                bot,
                chat_id=user_id,
                query_id=event.data['queryId'],
                message=WEEKDAY_HELP + wd_names[user.weekday],
                markup=WEEKDAY_INLINE,
            )
    else:
        if cb == 'days_eve':
            user.weekday = 'every'
            text = CORRECT_EVERYDAY
        else:
            user.weekday = 'monday'
            text = CORRECT_MONDAY
        user.save()
        set_schedule(bot, user)
        sender(
            bot,
            chat_id=user.user_id,
            msg_id=event.data['message']['msgId'],
            message=text,
        )


def end_streams(bot, event):
    sender(
        bot,
        chat_id=get_user_id(event),
        query_id=event.data['queryId'],
        msg_id=event.data['message']['msgId'],
        message=CORRECT_STREAMS,
    )


def stream_inline_keyboard(user_id):
    all_streams = [stream.name for stream in get_defined(Stream)]
    user, _ = BotUser.objects.get_or_create(user_id=user_id)
    user_streams = user.streams.all().values_list('name', flat=True)
    buttons = []
    for stream in all_streams:
        if stream in user_streams:
            stream += CHECKED
        buttons.append([{'text': stream, 'callbackData': f'streams_{stream}'}])
    buttons.append(
        [{'text': END_STREAMS, 'style': 'primary', 'callbackData': 'end_streams'}]
    )
    return buttons


def stream_selected(bot, event):
    stream = event.data["callbackData"].split('_')[-1]
    user, _ = BotUser.objects.get_or_create(user_id=get_user_id(event))
    if CHECKED in stream:
        stream = stream.replace(CHECKED, '')
        stream_id = Stream.objects.get(name=stream).pk
        user.streams.remove(stream_id)
    else:
        stream_id = Stream.objects.get(name=stream).pk
        user.streams.add(stream_id)
        stream += CHECKED
    sender(
        bot,
        chat_id=user.user_id,
        query_id=event.data['queryId'],
        msg_id=event.data['message']['msgId'],
        message=event.data['message']['text'],
        markup=stream_inline_keyboard(user.user_id),
    )


def stream_cb(bot, event):
    user_id = get_user_id(event)
    sender(
        bot,
        chat_id=user_id,
        query_id=event.data['queryId'],
        message=STREAMS_HELP,
        markup=stream_inline_keyboard(user_id),
    )


def time_inline_keyboard(item_name, value=None, msgid=''):
    if item_name == 'hour':
        range_item = (0, 24, 1)
        shape_item = (4, 6)
    else:
        if getenv('DEBUG_USER', default=False):
            range_item = (0, 60, 1)
            shape_item = (10, 6)
        else:
            range_item = (0, 31, 30)
            shape_item = (1, 2)
    item_name += f'_{value}' if value else '_'
    if msgid:
        msgid = ':' + msgid
    return list(
        list(i)
        for i in np.reshape(
            [
                {
                    'text': str(item).zfill(2),
                    'callbackData': f'{item_name}{str(item).zfill(2)}{msgid}',
                }
                for item in range(*range_item)
            ],
            shape_item,
        )
    )


def time_cb(bot, event):
    user_id = get_user_id(event)
    user, _ = BotUser.objects.get_or_create(user_id=user_id)
    cb = event.data["callbackData"]
    if cb == 'time_cb':
        sender(
            bot,
            chat_id=user_id,
            query_id=event.data['queryId'],
            message=TIME_START + (user.receiving_time or NO_TIME) + HOUR,
            markup=time_inline_keyboard('hour'),
        )
    elif cb.startswith('hour'):
        message_id = event.data['message']['msgId']
        hour = cb.split('_')[-1]
        sender(
            bot,
            chat_id=user_id,
            query_id=event.data['queryId'],
            msg_id=message_id,
            message=TIME_START + (user.receiving_time or NO_TIME) + MINUTES,
            markup=time_inline_keyboard('minute', hour, message_id),
        )
    elif cb.startswith('minute'):
        time_s, msgid = cb.split(':')
        time_s = time_s.split('_')[-1]
        time_s = time_s[:2] + ':' + time_s[2:]
        sender(bot, chat_id=user_id, msg_id=msgid, message=f'{CORRECT_TIME}{time_s}')
        user.is_active = True
        user.receiving_time = time_s
        user.save()
        set_schedule(bot, user)


def start_cb(bot, event):
    user, created = BotUser.objects.get_or_create(user_id=get_user_id(event))
    if created or not user.is_active:
        bot.send_text(chat_id=event.from_chat, text=FIRST_START)
        user.is_active = True
        user.save()
    else:
        bot.send_text(chat_id=event.from_chat, text=REPEAT_START)


def stop_cb(bot, event):
    BotUser.objects.filter(user_id=get_user_id(event)).update(is_active=False)
