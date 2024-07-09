from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_old_records import OldRecordsManager

from .constants import MAX_ADMIN_MESSAGE_LENGTH
from .functions import kw_forms, raw_text
from .validators import validate_pub_date


class Stream(models.Model):
    class CompanyChoices(models.TextChoices):
        MAILRU = 'mailru', _('Mail.ru')
        RUSTORE = 'rustore', _('Rustore')

    name = models.CharField(
        _('Название'),
        max_length=50,
    )
    company = models.CharField(
        max_length=15, verbose_name=_('Продукт'), choices=CompanyChoices.choices
    )
    is_active = models.BooleanField(
        _('Стрим Активирован?'),
        default=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'company'], name='unique stream')
        ]
        ordering = ['id']
        verbose_name = _('Стрим')
        verbose_name_plural = _('Стримы')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """В боте может отображаться только 14 кнопок.
        Поэтому введем ограничение на количество записей."""
        if Stream.objects.filter(is_active=True).count() >= 14:
            raise ValidationError(
                _(
                    'Максимальное количество кнопок в боте - 14. Поэтому Стримов может быть только 14.'
                )
            )
        else:
            super().save(*args, **kwargs)


class KeyWord(models.Model):
    class KeyWordTypeChoices(models.TextChoices):
        KW = 'key_word', _('Ключевое слово')
        AKW = 'add_key_word', _('Дополнительное ключевое слово')
        BL = 'blacklist', _('Черный список')
        BLOCK = 'blocklist', _('Блок-лист')

    name = models.CharField(
        max_length=100,
        verbose_name=_('Ключевое слово'),
        help_text=_(
            'Введите ключевое слово. Регистр не имеет значения. '
            'Пробелы и другие вспомогательные символы играют роль.'
        ),
    )
    kw_type = models.CharField(
        max_length=50,
        verbose_name=_('Тип поиска'),
        choices=KeyWordTypeChoices.choices,
        default=KeyWordTypeChoices.KW,
        help_text=_(
            'Если по ключевому слову не должен осуществляться поиск '
            'в источниках с широконаправленной тематикой новостей, '
            'выберите "Дополнительное". Если из новости должно быть '
            'исключено определенное слово, выберите "Черный список". '
            'Если должна быть исключена новость, состоящая только '
            'из выбранной фразы, выберите "Блок-лист"'
        ),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'kw_type'], name='unique keyword')
        ]
        ordering = [
            'name',
        ]
        verbose_name = _('Ключевое слово')
        verbose_name_plural = _('Ключевые слова и черный список')

    def __str__(self):
        kw_dict = {
            'key_word': '',
            'add_key_word': ' (доп.)',
            'blacklist': ' (ЧС)',
            'blocklist': ' (блок)',
        }
        return self.name + kw_dict[self.kw_type]

    def get_kw_forms(self):
        return kw_forms(self)


class Service(models.Model):
    name = models.CharField(_('Название'), max_length=100)
    key_words = models.ManyToManyField(
        KeyWord, verbose_name=_('Ключевые слова'), blank=True
    )
    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name=_('Стрим'),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'stream_id'], name='unique service')
        ]
        ordering = ['id']
        verbose_name = _('Сервис')
        verbose_name_plural = _('Сервисы')

    def __str__(self):
        return self.name


class Address(models.Model):
    address = models.URLField(_('Адрес сайта'), max_length=700, null=True, blank=True)
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name=_('Сервис'),
    )
    search_key_words = models.BooleanField(
        _('Искать по ключевым словам'), default=False
    )
    search_add_key_words = models.BooleanField(
        _('Искать по дополнительным ключевым словам'),
        help_text=_('*Если источник содержит новости различных сервисов'),
        default=False,
    )
    for_parser = models.BooleanField(_('Источник для парсера'), default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['address', 'service'], name='unique address for service'
            )
        ]
        verbose_name = _('Источник')
        verbose_name_plural = _('Источники')

    def __str__(self):
        return self.address

    @classmethod
    def get_not_defined(cls, address_address, company):
        stream, _ = Stream.objects.get_or_create(name='Не определен', company=company)
        service, _ = Service.objects.get_or_create(
            name='Не определен', stream_id=stream.pk
        )
        address, _ = cls.objects.get_or_create(
            address=address_address, service_id=service.pk, for_parser=False
        )
        return address


class News(models.Model):
    pub_date = models.DateField(_('Дата публикации'), validators=[validate_pub_date])
    title = models.CharField(_('Заголовок'), max_length=1000, null=True, blank=True)
    summary = models.TextField(_('Краткое описание'), null=True, blank=True)
    text = models.TextField(_('Текст новости'), null=True, blank=True)
    stream = models.ForeignKey(
        Stream, on_delete=models.CASCADE, verbose_name=_('Стрим')
    )
    image = models.ImageField(_('Фотография'), upload_to='news/', null=True, blank=True)
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Источник',
        blank=True,
        null=True,
    )
    url = models.URLField(_('Ссылка на новость'), max_length=700)
    is_moderated = models.BooleanField(_('Проверено модератором'), default=False)
    is_blacklisted = models.BooleanField(
        _('В черном списке'),
        default=False,
    )
    is_deleted = models.BooleanField(_('Больше не показывать новость'), default=False)

    objects = models.Manager()
    created_at_field = 'pub_date'
    max_age = 30
    old_records = OldRecordsManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'address'],
                # fields=['title', 'pub_date'],
                # include=['address', ],
                name='unique news item',
            ),
        ]
        ordering = ['-pub_date']
        verbose_name = _('Новость')
        verbose_name_plural = _('Новости')

    def __str__(self):
        return self.title or 'Без заголовка'

    def save(self, *args, **kwargs):
        self.stream = self.address.service.stream
        self.text = raw_text(self.text)
        super().save(*args, **kwargs)


class BotUser(models.Model):
    class WeekdayChoices(models.TextChoices):
        MON = 'monday', _('Понедельник')
        EVE = 'every', _('Каждый день')

    user_id = models.CharField(
        _('Уникальный ID пользователя VK Teams'),
        max_length=100,
        primary_key=True,
        unique=True,
    )
    streams = models.ManyToManyField(
        Stream, verbose_name=_('Список подписанных стримов'), blank=True
    )
    receiving_time = models.CharField(
        max_length=5, verbose_name=_('Время получения новостей'), null=True, blank=True
    )
    received_news = models.ManyToManyField(
        News, verbose_name=_('Полученные пользователем новости'), blank=True
    )
    is_superuser = models.BooleanField(
        verbose_name=_('Права администратора'),
        help_text=_('Администратор может получать новости ежедневно'),
        default=False,
    )
    is_active = models.BooleanField(default=True)
    weekday = models.CharField(
        max_length=50,
        choices=WeekdayChoices.choices,
        default=WeekdayChoices.MON,
        verbose_name=_('Получать по понедельникам или каждый день?'),
    )

    class Meta:
        verbose_name = _('Пользователь бота')
        verbose_name_plural = _('Пользователи бота')

    def __str__(self):
        return self.user_id

    def get_stream_names(self):
        return [stream.name for stream in self.streams.exclude(name='Не определен')]


class AdminMessage(models.Model):
    message = models.TextField(
        verbose_name=_('Сообщение'),
        blank=False,
        help_text=_('Это будет отправлено ВСЕМ юзерам'),
    )

    class Meta:
        verbose_name = _('Сообщение для всех')
        verbose_name_plural = _('Сообщения для всех')

    def __str__(self) -> str:
        return self.message[:MAX_ADMIN_MESSAGE_LENGTH]


def get_defined(model):
    return model.objects.exclude(name='Не определен')


def get_total_reaction(reaction):
    return models.Sum(
        models.Case(
            models.When(reaction=reaction, then=1),
            default=0,
            output_field=models.IntegerField(),
        )
    )


class Reaction(models.Model):
    class ReactionChoices(models.TextChoices):
        LK = 'like', _('')
        DL = 'dislike', _('')
        NR = 'no_reaction', _('')

    monday_date = models.DateField(verbose_name=_('Дата отправки новостей'))
    user = models.ForeignKey(
        BotUser,
        on_delete=models.SET_NULL,
        related_name='users',
        blank=True,
        null=True,
        verbose_name=_('Пользователь, поставивший реакцию'),
    )
    reaction = models.CharField(
        max_length=50, default=ReactionChoices.NR, verbose_name=_('Реакция')
    )
    news_temp = models.TextField(
        verbose_name=_(
            'Поле для сохранения текста рассылки, '
            'чтобы не потерять формат при нажатии лайка/дизлайка'
        )
    )

    class Meta:
        verbose_name = _('Реакция')
        verbose_name_plural = _('Реакции на новости')
        ordering = ['-monday_date']
        constraints = [
            models.UniqueConstraint(
                fields=['monday_date', 'user'], name='unique reaction'
            ),
        ]

    def __str__(self):
        return self.monday_date.isoformat()

    def get_monday_date_likes(self):
        qs = Reaction.objects.filter(monday_date=self.monday_date)
        likes = qs.aggregate(likes=get_total_reaction('like'))
        return likes.get('likes') or 0

    get_monday_date_likes.short_description = _('Количество лайков')

    def get_monday_date_dislikes(self):
        qs = Reaction.objects.filter(monday_date=self.monday_date)
        dislikes = qs.aggregate(dislikes=get_total_reaction('dislike'))
        return dislikes.get('dislikes') or 0

    get_monday_date_dislikes.short_description = _('Количество дизлайков')

    def get_monday_date_no_reaction(self):
        qs = Reaction.objects.filter(monday_date=self.monday_date)
        no_reaction = qs.aggregate(no_reaction=get_total_reaction('no_reaction'))
        return no_reaction.get('no_reaction') or 0

    get_monday_date_no_reaction.short_description = _('Количестов реакций без ответа')
