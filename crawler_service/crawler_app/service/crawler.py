import requests
from bs4 import BeautifulSoup
import tldextract
from urllib.parse import urljoin
from crawler_app.utils.robot_parser_util import CrawlerRobotParserUtil
from crawler_app.utils.common_util import is_website_reachable
from crawler_exceptions.exceptions import WebsiteNotReachableException, CrawlNotAllowedException
import logging

logger = logging.getLogger(__name__)

class Crawler:
    
    FEED_PATHS = ['/rss', '/feed', 'xml/rss/all.xml', '/feed/rss']

    def __init__(self, url):
        self.url = url
        self.rss_links = set()
        self.outgoing_domains = set()
        self.domain = tldextract.extract(url).domain

    
    def crawl(self):
        logger.info("Crawler Started For Website:%s\n" %(self.url))
        if not is_website_reachable(self.url):
            raise WebsiteNotReachableException()
        logger.info("Verifying robots.txt to ensure crawling is allowed.")
        crlr_checker = CrawlerRobotParserUtil(self.url)
        if not crlr_checker.crawl_allowed():
            raise CrawlNotAllowedException()
        self.response = ""
        self.soup = None

        self.__initialise_bs4()
        self.__extract_rss_feed_from_path()
        self.__extract_rss_feeds_from_html()
        self.__get_outgoing_domains()
        logger.info("Ended Crawling For URL: %s.\n" %(self.url))
        logger.info("---------------------------------------------------------")


    def __initialise_bs4(self):
        self.response = requests.get(self.url)
        if self.response.status_code != 200:
            raise WebsiteNotReachableException()
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def __extract_rss_feed_from_path(self):
        logger.info("Finding whether feeds exists in common rss paths...\n")
        rss_feeds = set()
        for path in self.FEED_PATHS:
            feed_url = urljoin(self.url, path)
            response_feed = requests.head(feed_url)
            if response_feed.status_code == 200:
                rss_feeds.add(feed_url)
        if rss_feeds:
            logger.info("Feeds in path:%s" %list(rss_feeds))
        self.rss_links = self.rss_links.union(rss_feeds)
        
    def __extract_rss_feeds_from_html(self):
        logger.info("Parsing html to find feeds...\n")
        rss_feeds = set()
        for link_tag in self.soup.find_all('link', {'type': 'application/rss+xml'}):
                rss_feeds.add(urljoin(self.url, link_tag.get('href')))
        if rss_feeds:
            logger.info("Feeds from HTML:%s" %list(rss_feeds))
            self.rss_links = self.rss_links.union(rss_feeds)


    def __get_outgoing_domains(self):
        logger.info("Parsing html to find outgoing domains...\n")

        for a in self.soup.find_all('a', href=True):
            link_tld = tldextract.extract(a.get('href'))
            if not(link_tld.domain and link_tld.suffix):
                continue
            if link_tld.domain != self.domain:
                link_tld.subdomain = link_tld.subdomain or 'www'
                self.outgoing_domains.add('https://' + link_tld.subdomain + '.' + link_tld.domain + '.' + link_tld.suffix)
        if self.outgoing_domains:
            logger.info("Outgoing domains are:%s" %list(self.outgoing_domains))

    def get_feeds(self):
        return list(self.rss_links)
    
    def get_outgoing_domains(self):
        return list(self.outgoing_domains)