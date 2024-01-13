import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from urllib.parse import urlparse
from crawler.items import FeedItem

class FeedURLSpider(CrawlSpider):
    name = 'feeds'
    custom_settings = { 
      'DEPTH_LIMIT': 1, 
     }

    def __init__(self, *args, **kwargs):
        super(FeedURLSpider, self).__init__(*args, **kwargs)
        self.feed_urls = set()  # Store feed URLs in a set to avoid duplicates
        self.start_url = kwargs.get('start_url', 'https://tastecooking.com')



    rules = (
        Rule(LinkExtractor(allow=('/rss', '/feed')), callback='parse_feed_link', follow=False),
        Rule(LinkExtractor(), callback='parse_external_links', follow=True),
    )

    feed_links = []
    external_domain_links = []

    def parse_feed_link(self, response):
        if response.status == 200:
            self.feed_links.append(response.url)

    def parse_external_links(self, response):
        if response.url.split('://')[1].split('/')[0] not in self.allowed_domains:
            self.external_domain_links.append(response.url)