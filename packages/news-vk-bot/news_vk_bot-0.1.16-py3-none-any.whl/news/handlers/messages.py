import re
from os import getenv

from django.db.models import Q
from dotenv import load_dotenv

from news.models import Stream

load_dotenv()

HELP = [
    [{'text': 'Установите время получения новостей', 'callbackData': 'time_cb'}],
    [
        {
            'text': 'Просмотр и редактирование\nподписок на стримы',
            'callbackData': 'stream_cb',
        }
    ],
]
HELP_TEXT = (
    'Бот новостной рассылки из сферы IT. Настройте бот и получайте '
    'новости по понедельникам. Пожалуйста, оставьте оценку, '
    'воспользовавшись кнопками под новостной рассылкой - нам важно '
    'Ваше мнение!\n\n'
    '/feedback - обратная связь\n\nВыберите настройки бота:'
)

FIRST_START = (
    'Настройте время получения новостей (в понедельник) и стримы.\n'
    'Введите /help для просмотра всех возможностей бота'
)
REPEAT_START = (
    'Вы уже начали работу с ботом. Можете настроить время '
    'получения новостей и стримы. По умолчанию они не установлены'
    '\nВведите /help для просмотра всех возможностей бота'
)

TIME_START = (
    'Установите время получения новостей (по московскому времени, '
    'в понедельник). Если не установить время, новости не будут '
    'отправляться.\nСейчас: '
)
NO_TIME = 'время не выбрано'
CORRECT_TIME = 'Время установлено: '
HOUR = '\n\nВыберите час получения:'
MINUTES = '\n\nВыберите минуту получения:'

STREAMS_HELP = 'Просмотр и редактирование подписок на стримы:'
CORRECT_STREAMS = 'Стрим(ы) успешно обработан(ы)!'
END_STREAMS = 'Сохранить изменения'

WEEKDAY_HELP = (
    'Здесь можно настроить день получения новостной рассылки: '
    'в понедельник (по умолчанию) или ежедневно. Сейчас : '
)
WEEKDAY_OPTIONS = [{'text': 'По понедельникам/ежедневно', 'callbackData': 'weekday_cb'}]
WEEKDAY_INLINE = [
    [{'text': 'По понедельникам (по умолчанию)', 'callbackData': 'days_mon'}],
    [{'text': 'Каждый день', 'callbackData': 'days_eve'}],
]
CORRECT_EVERYDAY = 'Теперь новости будут приходить ежедневно.'
CORRECT_MONDAY = 'Теперь новости будут приходить по понедельникам.'
CHOOSE_TIME = 'Сначала нужно выбрать время получения!'

FEEDBACK_MESSAGE = 'Обратная связь от {source}: {message}'
FEEDBACK_SENT = 'Сообщение отправлено администраторам!'
FEEDBACK_ERROR = (
    'Введите в формате (без кавычек):\n'
    '"/feedback Возможно, стоит подобрать эмодзи кругов другого '
    'цвета для стримов"'
)

REACTION_ANSWER = 'Спасибо за вашу оценку!'


def news_post(news):
    def html_prep(text):
        if text:
            return text.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
        return ''

    def service_name(news_item):
        return re.sub(r'\s\([А-Яа-я]+\)', '', news_item.address.service.name)

    def text_prep(news_item):
        if news_item.title:
            return news_item.title
        if news_item.summary:
            return news_item.summary
        return news_item.text

    def get_message_text(url, news_item):
        return (
            f'- <a href="{url}">'
            f'{service_name(news_item)}</a>: '
            f'{html_prep(text_prep(news_item)) or ""}\n'
        )

    message = ''
    for company_name in Stream.CompanyChoices.choices:
        company_name = company_name[0]
        company = news.filter(stream__company=company_name)
        if company:
            message += f'\U0001F535<strong>{company_name.capitalize()}</strong>\n'
            for stream in set(company.values_list('stream__name', flat=True)):
                message += f'\u26AAСтрим: <strong>{stream}</strong>\n'
                for news_item in company.filter(Q(stream__name=stream)):
                    message += get_message_text(news_item.url, news_item)
                message += '\n'
    return message.strip('\n')


NO_NEWS = 'Новостей нет'
NO_STREAMS = 'Новостей нет. Выберите стримы, чтобы еженедельно ' 'получать новости'
