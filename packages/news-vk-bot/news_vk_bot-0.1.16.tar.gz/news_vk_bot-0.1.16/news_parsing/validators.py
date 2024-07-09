from news.models import News


def unique_vc(obj):
    if News.objects.filter(
        address__address__contains='https://vc.ru',
        url=obj['url'],
        stream__name=obj['stream'].name,
        is_blacklisted=False,
    ):
        return False
    if obj['is_blacklisted'] is False:
        News.objects.filter(
            address__address__contains='https://vc.ru',
            url=obj['url'],
            is_blacklisted=True,
        ).delete()
    return True
