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


    feed_links = set()
    external_domain_links = set()


    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse)

    def parse(self, response):
        for path in ['/rss', '/feed', '/feed/rss']:
            url_to_check = response.urljoin(path)
            yield scrapy.Request(url_to_check, callback=self.parse_feed_link)
        
        external_link_extractor = LinkExtractor(deny_domains=(self.domains_allowed))
        external_links = external_link_extractor.extract_links(response)
        for link in external_links:
            self.external_domain_links.add(self.get_domain(link.url))

        internal_link_extractor = LinkExtractor(allow_domains=(self.domains_allowed))
        internal_links = internal_link_extractor.extract_links(response)
        for link in internal_links:
            yield scrapy.Request(link.url, callback=self.parse)



    def parse_feed_link(self, response):
        if response.status == 200:
            self.feed_links.add(response.url)


    def close(self, reason):
        print('\nFeed Links:')
        print(self.feed_links)
        print('\External Links:')
        print(self.external_domain_links)


    def get_domain(self,url):
        return URLUtil.get_domain(url)