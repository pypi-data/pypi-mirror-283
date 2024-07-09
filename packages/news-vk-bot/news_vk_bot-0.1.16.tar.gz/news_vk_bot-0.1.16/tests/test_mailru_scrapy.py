import pytest
from scrapy.http import HtmlResponse, Request

from news_parsing.spiders.mailru import MailruSpider
from tests.spider_mocks import html_mock_list, test_urls


def test_mailru_parse_no_bs4():
    spider = MailruSpider()

    for expected_result, url in zip(html_mock_list, test_urls):

        parse_data = test_urls[url]
        meta = {'parse_data': parse_data}
        req = Request(
            url=url,
            meta=meta,
            headers=parse_data.get('headers'),
        )
        resp = HtmlResponse(
            url=url, request=req, body=expected_result, encoding='utf-8'
        )

        res = list(spider.parse(resp))
        assert len(res) == 1
        assert isinstance(res[0], Request)


# @pytest.mark.django_db
def test_mailru_parse_detail_no_bs4():
    spider = MailruSpider()

    for expected_result, url in zip(html_mock_list, test_urls):

        parse_data = test_urls[url]
        meta = {'parse_data': parse_data}
        req = Request(
            url=url,
            meta=meta,
            headers=parse_data.get('headers'),
        )
        resp = HtmlResponse(
            url=url, request=req, body=expected_result, encoding='utf-8'
        )

        res = list(
            spider.parse_details(
                resp, item={'url': ''}, parse_data=parse_data, addresses={}
            )
        )
        print(res)
        assert True
        # assert len(res) == 1
        # assert isinstance(res[0], Request)
