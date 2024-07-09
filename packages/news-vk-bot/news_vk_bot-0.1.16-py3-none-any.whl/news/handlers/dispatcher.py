import logging
import os
import time
from http.client import RemoteDisconnected
from signal import SIGABRT, SIGINT, SIGTERM, signal
from sys import stdout

import schedule
from bot.bot import Bot, InvalidToken
from bot.filter import Filter
from bot.handler import (BotButtonCommandHandler, CommandHandler,
                         FeedbackCommandHandler, HelpCommandHandler,
                         MessageHandler, StartCommandHandler)
from dotenv import load_dotenv
from requests.exceptions import ConnectionError
from urllib3.exceptions import ProtocolError, ReadTimeoutError

from monitoring.metrics import (IS_BOT_ALIVE, get_current_number_of_news,
                                get_current_number_of_users,
                                start_capturing_metrics)
from news.models import BotUser

from .commands import (dislike_cb, end_streams, help_cb, like_cb,
                       notify_every_user, set_schedule, start_cb, stop_cb,
                       stream_cb, stream_selected, time_cb, weekday_cb)
from .messages import FEEDBACK_ERROR, FEEDBACK_MESSAGE, FEEDBACK_SENT

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=stdout)
logger.addHandler(handler)


class FeedbackCommandHandler(FeedbackCommandHandler):
    def message_cb(self, bot, event):
        source = event.data['chat']['chatId']
        feedback_text = event.data["text"].partition(" ")[2].strip()
        if feedback_text:
            for target in self.target:
                bot.send_text(
                    chat_id=target,
                    text=self.message.format(source=source, message=feedback_text),
                )
            if self.reply is not None:
                bot.send_text(chat_id=source, text=self.reply)
        elif self.error_reply is not None:
            bot.send_text(chat_id=source, text=self.error_reply)


class Bot(Bot):
    def _signal_handler(self, sig, _):
        super()._signal_handler(sig)


bot = Bot(
    os.getenv('BOT_TOKEN'),
    name='news-mail-bot',
    api_url_base=os.getenv('API_URL_BASE'),
    is_myteam=os.getenv('MYTEAM'),
)

ADMIN_IDS = os.getenv('ADMIN_IDS').split(';')


def set_dispatcher():
    bot.dispatcher.add_handler(StartCommandHandler(callback=start_cb))
    bot.dispatcher.add_handler(HelpCommandHandler(callback=help_cb))
    bot.dispatcher.add_handler(
        FeedbackCommandHandler(
            target=ADMIN_IDS,
            message=FEEDBACK_MESSAGE,
            reply=FEEDBACK_SENT,
            error_reply=FEEDBACK_ERROR,
        )
    )
    bot.dispatcher.add_handler(
        MessageHandler(
            callback=help_cb,
            filters=~Filter.regexp(r'^\s*(\/start|\/stop|\/help|\/feedback)'),
        )
    )
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=weekday_cb, filters=Filter.callback_data('weekday_cb')
        )
    )
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=like_cb, filters=Filter.callback_data_regexp('like_.*')
        )
    )
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=dislike_cb, filters=Filter.callback_data_regexp('dislike_.*')
        )
    )
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=weekday_cb, filters=Filter.callback_data_regexp('days_.*')
        )
    )
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=time_cb, filters=Filter.callback_data('time_cb')
        )
    )
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=time_cb, filters=Filter.callback_data_regexp('hour_.*|minute_.*')
        )
    )
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=stream_cb, filters=Filter.callback_data('stream_cb')
        )
    )
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=stream_selected, filters=Filter.callback_data_regexp('streams_.*')
        )
    )
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=end_streams, filters=Filter.callback_data('end_streams')
        )
    )
    bot.dispatcher.add_handler(CommandHandler(command='stop', callback=stop_cb))
    return bot


@IS_BOT_ALIVE.track_inprogress()
def idle(bot):
    for sig in (SIGINT, SIGTERM, SIGABRT):
        signal(sig, bot._signal_handler)

    while bot.running:
        for user in BotUser.objects.filter(is_active=True):
            try:
                if schedule.get_jobs(user.user_id)[0] not in (
                    schedule.get_jobs(user.weekday)
                ):
                    set_schedule(bot, user)
            except IndexError as exc:
                print(exc)
                set_schedule(bot, user)

        schedule.run_pending()
        time.sleep(1)


def send_admin_message_dispatch(queryset):
    notify_every_user(bot, queryset)


def run_polling():
    get_current_number_of_users()
    get_current_number_of_news()
    start_capturing_metrics()
    try:
        bot = set_dispatcher()
        for user in BotUser.objects.filter(is_active=True):
            if user.receiving_time:
                set_schedule(bot, user)
        bot.start_polling()
        idle(bot)
    except (
        KeyError,
        ProtocolError,
        ReadTimeoutError,
        InvalidToken,
        ConnectionError,
        RemoteDisconnected,
    ):
        logging.error('API access error')
        # logging.error(e)
