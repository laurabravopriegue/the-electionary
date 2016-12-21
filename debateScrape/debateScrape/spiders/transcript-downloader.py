# Transcript Downloader
# Downloads from a specified list of URLs
# Then saves them all to disk

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import json
import os

class MySpider(BaseSpider):
    # Name the spider as required by scrapy
    name = "download"
    
    # Set a download delay of 5 seconds.
    # This makes the downloads take longer, but it's kinder on the UCSB servers.
    download_delay = 5

    # Import the list of URLs to download from - this comes from our earlier file.
    with file('urls.json', 'r') as f:
        start_urls = json.load(f)
    
    # Once again, the allowed domain is set.
    allowed_domains = ['ucsb.edu']
    
    # parse method, run every time the spider is run
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        # The only purpose of the following code is to give the files sensible names.
        
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
        
        
        # The files are then saved to a directory, for access later.
        with open(os.path.join('html-files', fileName), 'w') as f:
            f.write(response.body)
