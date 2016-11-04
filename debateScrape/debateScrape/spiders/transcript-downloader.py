# Transcript Downloader
# Downloads from a specified list of URLs
# Then saves them all to disk

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import json
import os

class MySpider(BaseSpider):
    name = "download"
    download_delay = 5

    with file('urls.json', 'r') as f:
        startData = json.load(f)

    allowed_domains = startData["allowed_domains"]
    start_urls = startData["start_urls"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        # Extract the date of the debate
        date = hxs.select("//span[@class='docdate']/text()").extract()
        for date in date:
            debateDate = date
            break

        # Extract the name description of the debate
        name = hxs.select("//span[@class='paperstitle']/text()").extract()
        for name in name:
            debateName = name
            break

        fileName = debateDate + " " + debateName + ".html"

        with open(os.path.join('html-files', fileName), 'w') as f:
            f.write(response.body)