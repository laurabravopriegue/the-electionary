# URL Fetcher
# Fetches a list of URLs to be used by Transcript Processor

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import json

class MySpider(BaseSpider):
    name = "urlfetch"

    with file('url.txt', 'r') as f:
        url = f.read()

    allowed_domains = ["ucsb.edu"]
    start_urls = [url]

    def parse(self, response):

        hxs = HtmlXPathSelector(response)

        urls = hxs.select("//td[@class='doctext']/a/@href").extract()

        dictionary = {"allowed_domains": allowed_domains, "start_urls": urls}

        with open('urls.json', 'w') as f:
            json.dump(dictionary, f)