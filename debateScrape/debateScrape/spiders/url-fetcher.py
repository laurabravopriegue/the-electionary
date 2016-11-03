# URL Fetcher
# Fetches a list of URLs to be used by Transcript Processor

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import json

class MySpider(BaseSpider):
    name = "geoffrey"

    with file('urls.json', 'r') as f:
        startData = json.load(f)
    with file('url.txt', 'r') as f:
        url = f.read()

    allowed_domains = startData["allowed_domains"]
    start_urls = [url]

    def parse(self, response):

        with file('urls.json', 'r') as f:
            startData = json.load(f)
        allowed_domains = startData["allowed_domains"]

        hxs = HtmlXPathSelector(response)

        urls = hxs.select("//td[@class='doctext']/a/@href").extract()

        dictionary = {"allowed_domains": allowed_domains, "start_urls": urls}

        with open('urls.json', 'w') as f:
            json.dump(dictionary, f)