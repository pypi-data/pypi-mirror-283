from django.core.exceptions import ValidationError
from django.utils import timezone as tz


def validate_pub_date(value):
    current_year = tz.now().year - 1
    if current_year > value.year:
        raise ValidationError('Слишком старая новость')
