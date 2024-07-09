import logging

from prometheus_client import Counter, Gauge, Histogram, start_http_server

from monitoring.constants import PORT_OF_METRIC_GATHERING
from news.models import BotUser, News

SENT_MESSAGES = Counter(
    'bot_sent_messages_total', 'Number of messages the bot has sent'
)

SENT_EVERYDAY = Counter(
    'bot_sent_messages_everyday_total',
    'Number of messages the bot has sent for users that chose "everyday" option',
)

SENT_ON_MONDAY = Counter(
    'bot_sent_messages_on_monday_total',
    'Number of messages the bot has sent for users on monday',
)

TIME_TO_SEND_A_MESSAGE = Histogram(
    'bot_time_to_send_a_message_seconds', 'Time it took for a bot to send a message'
)

NUMBER_OF_NO_NEWS = Counter(
    'bot_number_of_no_news_total', 'Number of times there has been no news to send'
)

NUMBER_OF_LIKES = Counter(
    'bot_numer_of_likes_of_news_total', 'Number of times the user has liked the news'
)

NUMBER_OF_DISLIKES = Counter(
    'bot_numer_of_dislikes_of_news_total',
    'Number of times the user has disliked the news',
)

NUMBER_OF_ERRORS_IN_SENDER = Counter(
    'bot_number_of_exceptions_message_sending_total',
    'Number of exceptions that have occured during message sending',
)

NUMBER_OF_NEWS = Gauge('bot_number_of_news_current', 'Current number of news for users')

ALL_USERS_ADMIN_NOTIFICATION = Gauge(
    'bot_all_users_notification_current', 'Are all users being notified by an admin'
)

NUMBER_OF_ERRORS_IN_ALL_USERS_ADMIN_NOTIFICATION = Counter(
    'bot_nubmer_of_exceptions_all_users_notification_total',
    'Number of exceptons that have occured during notifying all users by an admin',
)


NUMBER_OF_CURRENT_USERS = Gauge(
    'bot_number_of_users_current', 'Number of current users of the bot'
)

IS_BOT_ALIVE = Gauge(
    'bot_health_current', 'Metric to check whether or not bot is alive'
)


def get_current_number_of_news():
    try:
        NUMBER_OF_NEWS.set(News.objects.all().count())
    except Exception as e:
        logging.error(f'Error getting number of news: {e}')


def get_current_number_of_users():
    try:
        NUMBER_OF_CURRENT_USERS.set(BotUser.objects.filter(is_active=True).count())
    except Exception as e:
        logging.error(f'Error getting number of current user: {e}')


def start_capturing_metrics():
    start_http_server(PORT_OF_METRIC_GATHERING)
