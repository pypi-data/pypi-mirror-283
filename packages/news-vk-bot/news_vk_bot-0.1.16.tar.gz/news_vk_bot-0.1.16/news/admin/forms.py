from functools import partial
from itertools import groupby
from operator import attrgetter

from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from ..models import Address, News, Service, get_defined


class GroupedModelChoiceIterator(forms.models.ModelChoiceIterator):
    def __init__(self, field, groupby):
        self.groupby = groupby
        super().__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ('', self.field.empty_label)
        queryset = self.queryset
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
            for group, objs in groupby(queryset, self.groupby):
                yield (group, [self.choice(obj) for obj in objs])


class GroupedModelChoiceField(forms.models.ModelChoiceField):
    def __init__(self, *args, choices_groupby, **kwargs):
        if isinstance(choices_groupby, str):
            choices_groupby = attrgetter(choices_groupby)
        elif not callable(choices_groupby):
            raise TypeError(
                'choices_groupby must either be a str or '
                'a callable accepting a single argument'
            )
        self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
        super().__init__(*args, **kwargs)


class NewsAdminForm(forms.ModelForm):
    text = forms.CharField(label=_('Текст новости'), widget=TinyMCE, required=False)
    service = GroupedModelChoiceField(
        label=_('Стрим и сервис'),
        queryset=Service.objects.all(),
        choices_groupby='stream',
    )

    class Meta:
        model = News
        fields = (
            'pub_date',
            'is_moderated',
            'is_blacklisted',
            'service',
            'title',
            'summary',
            'text',
            'url',
            'image',
        )

    def __init__(self, *args, **kwargs):
        self.base_fields['service'].initial = kwargs['instance'].address.service.id
        super().__init__(*args, **kwargs)

    def save(self, commit=False):
        news = super().save(commit=False)
        news.address = Address.objects.get(
            address=news.address.address, service=self.cleaned_data['service']
        )
        return news


class NewsCreationForm(forms.ModelForm):
    title = forms.CharField(label=_('Заголовок'))
    text = forms.CharField(label=_('Текст новости'), widget=TinyMCE, required=False)
    service = GroupedModelChoiceField(
        label=_('Стрим и сервис'),
        queryset=Service.objects.all(),
        choices_groupby='stream',
    )
    address_url = forms.URLField(label=_('Ссылка на новость'), required=False)

    class Meta(NewsAdminForm.Meta):
        model = News
        fields = (
            'pub_date',
            'is_moderated',
            'service',
            'title',
            'summary',
            'text',
            'image',
            'address_url',
        )

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            self.base_fields['service'].initial = kwargs['instance'].address.service.id
        else:
            self.base_fields['service'].initial = None
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        news = super().save(commit=False)
        address = self.cleaned_data['address_url']
        if not (address is None):
            address_service = Address.objects.filter(
                service=self.cleaned_data['service']
            )
            for addr in address_service.values_list('address', flat=True):
                if address.startswith(addr.strip('/')):
                    news.address = address_service.get(address=addr)
                    news.url = address
                    news.save()
                    return news
        news.address = Address.objects.create(
            address=address, service=self.cleaned_data['service'], for_parser=False
        )
        news.url = address
        news.save()
        return news
