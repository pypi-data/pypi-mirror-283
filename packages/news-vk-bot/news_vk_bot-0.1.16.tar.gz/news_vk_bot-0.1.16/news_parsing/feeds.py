from urllib.parse import urlparse

from news.models import Address, News


def stat():
    try:
        with open('stat.txt', 'w') as f:
            f.write('Null sources:')
            for source in set(Address.objects.all().values_list('address'), flat=True):
                url = urlparse(source).netloc
                if url.startswith('www.'):
                    url = url[4:]
                if len(News.objects.filter(address__address__contains=url)) == 0:
                    f.write(f'{url}\n')
    except Exception:
        pass
