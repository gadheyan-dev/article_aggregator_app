import requests
from bs4 import BeautifulSoup
import tldextract
from urllib.parse import urljoin
from crawler_app.utils.robot_parser_util import CrawlerRobotParserUtil

class WebsiteNotReachableException(Exception):
    pass


class Crawler:
    
    FEED_PATHS = ['/rss', '/feed', 'xml/rss/all.xml', '/feed/rss']

    def __init__(self, url):
        self.url = url
        self.rss_links = set()
        self.outbound_domains = set()
        self.domain = tldextract.extract(url).domain

    
    def crawl(self):
        print("Started Crawling...\n")
        print("Checking if crawling allowed for url:%s...\n" %(self.url))
        crlr_checker = CrawlerRobotParserUtil(self.url)
        if not crlr_checker.crawl_allowed():
            print("Crawling not allowed in this url... exiting...\n")
            return None

        self.response = ""
        self.soup = None
        try:
            self.__initialise_bs4()
        except (requests.RequestException, WebsiteNotReachableException) as e:
            print(f"Error accessing {self.url}: {e}")
            return

        self.__get_common_feeds()
        self.__get_all_rss_feeds()
        self.__get_outbound_domains()
        print("Ended Crawling")



    def __initialise_bs4(self):
        self.response = requests.get(self.url)
        if self.response.status_code != 200:
            raise WebsiteNotReachableException("Could not reach website")
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def __get_common_feeds(self):
        for path in self.FEED_PATHS:
            feed_url = urljoin(self.url, path)
            response_feed = requests.head(feed_url)
            if response_feed.status_code == 200:
                self.rss_links.add(feed_url)

    def __get_all_rss_feeds(self):
        for link_tag in self.soup.find_all('link', {'type': 'application/rss+xml'}):
                self.rss_links.add(urljoin(self.url, link_tag.get('href')))


    def __get_outbound_domains(self):
        # links = [a.get('href') for a in self.soup.find_all('a', href=True)]
        for a in self.soup.find_all('a', href=True):
            link_tld = tldextract.extract(a.get('href'))
            if not(link_tld.domain and link_tld.suffix):
                continue
            if link_tld.domain != self.domain:
                link_tld.subdomain = link_tld.subdomain or 'www'
                self.outbound_domains.add('https://' + link_tld.subdomain + '.' + link_tld.domain + '.' + link_tld.suffix)

    def get_feeds(self):
        return self.rss_links
    
    def get_outbound_domains(self):
        return self.outbound_domains