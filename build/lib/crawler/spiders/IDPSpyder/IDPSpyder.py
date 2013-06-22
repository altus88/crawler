__author__ = 'Gena'
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from crawler.items import IDPItem
from scrapy.webservice import JsonRpcResource
from scrapy.stats import stats

class StatsResource(JsonRpcResource):
    ws_name = 'stats'
    def __init__(self, crawler):
        JsonRpcResource.__init__(self, crawler, stats)

class IDPSpyder(BaseSpider):
    name = "idpspy"
    start_urls = [
        "http://www.in.tum.de/en/for-students-of-the-tum/master-programs/informatics/idp-offers.html"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        download_parts = hxs.select('//div[@class = "download"]//a')
        items = []
        for site in download_parts:
            item = IDPItem()
            item['title'] = site.select('text()').extract()
            item['link'] = site.select('@href').extract()
            items.append(item)
            print item

        return items

