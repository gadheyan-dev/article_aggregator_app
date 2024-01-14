import scrapy
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor

from crawler.items import FeedItem
from crawler.utils.url_util import URLUtil

class FeedURLSpider(Spider):
   
    name = 'feeds'
    custom_settings = {
      'DEPTH_LIMIT': 1, 
     }
    start_url = ""

    def __init__(self, *args, **kwargs):
        super(FeedURLSpider, self).__init__(*args, **kwargs)
        self.start_url = kwargs.get('start_url', 'https://tastecooking.com')
        self.domains_allowed = [self.get_domain(self.start_url)]
        self.feed_links = []


    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse)

    def parse(self, response):
        for path in ['/rss', '/feed', '/feed/rss']:
            url_to_check = response.urljoin(path)
            yield scrapy.Request(url_to_check, callback=self.parse_feed_link)

        link_extractor = LinkExtractor(allow_domains=(self.domains_allowed))
        links = link_extractor.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse)



    def parse_feed_link(self, response):
        feed_item = FeedItem()
        if response.status == 200:
            feed_item['url'] = response.url
            self.feed_links.append(feed_item)


    def close(self, reason):
        print('\nFeed Links:')
        print(self.feed_links)



    def get_domain(self,url):
        return URLUtil.get_domain(url)