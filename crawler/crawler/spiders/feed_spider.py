import scrapy
from utils import Util

class FeedSpider(scrapy.Spider):
    name = 'rss_spider'
    website_url = "https://www.bbc.com/"
    util = Util(website_url)

    def start_requests(self):
        if ! self.util.feed_exists():
            return None
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass