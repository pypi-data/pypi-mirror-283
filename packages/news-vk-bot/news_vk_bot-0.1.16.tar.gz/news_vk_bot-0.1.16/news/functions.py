import re
import warnings

import pymorphy2
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


def kw_forms(self):
    kw_list = [
        self.name.lower(),
    ]
    if re.search('[A-Яа-я]', self.name):
        morph = pymorphy2.MorphAnalyzer()
        kw_normal = kw_list[0].split()
        for form in ('nomn', 'gent', 'datv', 'accs', 'ablt', 'loct'):
            kw_list.append(
                ' '.join(
                    [
                        (
                            morph.parse(kw)[0].inflect({form}).word
                            if (
                                re.search('[A-Яа-я]', kw)
                                and (
                                    {'NOUN'} in morph.parse(kw)[0].tag
                                    or ({'ADJF'} in morph.parse(kw)[0].tag)
                                )
                            )
                            else kw
                        )
                        for kw in kw_normal
                    ]
                )
            )
        return set(kw_list)
    return kw_list


def preview(self):
    if self.image:
        image = get_thumbnail(
            self.image, '200x200', upscale=False, crop=False, quality=100
        )
        return format_html(
            f'<img src="{image.url}" ' f'width="{image.width}" height="{image.height}">'
        )
    return 'Фото не сохранено'


def raw_text(text):
    return BeautifulSoup(text or '', 'lxml').get_text() or ''
