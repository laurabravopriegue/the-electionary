# URL Fetcher
# Fetches a list of URLs to be used by transcript-downloader.py

# Import BaseSpider and HtmlXPathSelector from scrapy
# Also import JSON so we can export the file for later use

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import json

# MySpider instantiates BaseSpider
class MySpider(BaseSpider):
    
    # The spider must be named so we can call it later from Terminal
    name = "urlfetch"
    
    # We tell scrapy where to start the crawl, and which domains are allowed
    allowed_domains = ["ucsb.edu"]
    start_urls = ["http://www.presidency.ucsb.edu/debates.php"]
    
    # response is something that scrapy generates when the spider is run
    # scrapy will automatically call this method when the spider is run
    def parse(self, response):
        
        # HtmlXPathSelector is instantiated with the response
        hxs = HtmlXPathSelector(response)
        
        # The relevant urls are extracted from the HTML response
        # The string is an XPath statement
        # //td[@class='doctext'] means select all <td> elements in the HTML that have class attribute equal to 'doctext'
        # This selects elements like <td class='doctext'/>
        # In this case, there is only one such element
        # /a/@href means select the href attribute from any <a> element in this
        # e.g. <a href='www.example.com'>
        # .extract() then extracts the text element from this, and returns a list
        urls = hxs.select("//td[@class='doctext']/a/@href").extract()

        # Save the list of URLs to a JSON file
        with open('urls.json', 'w') as f:
            json.dump(urls, f)
