import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Crawler:
    
    FEED_PATHS = ['/rss', '/feed']

    def __init__(self, url):
        self.url = url
        self.rss_links = []
        self.__get_feeds_from_url()
        self.crawl()

    def crawl(self):

        try:
            response = requests.get(self.url)
            if response.status_code != 200:
                return
            soup = BeautifulSoup(response.content, 'html.parser')
            for link_tag in soup.find_all('link', {'type': 'application/rss+xml'}):
                    self.rss_links.append(urljoin(self.url, link_tag.get('href')))
           
            for link in soup.find_all('a', href=True):
                print(link['href'])

            # for a_tag in soup.find_all('a', href=True):
            #     next_url = urljoin(url, a_tag['href'])
            #     self.crawl(next_url)
        except requests.RequestException as e:
            print(f"Error accessing {self.url}: {e}")

    def __get_feeds_from_url(self):
        
        for path in self.FEED_PATHS:
            feed_url = urljoin(self.url, path)
            response_feed = requests.head(feed_url)
            if response_feed.status_code == 200:
                self.rss_links.append(feed_url)
