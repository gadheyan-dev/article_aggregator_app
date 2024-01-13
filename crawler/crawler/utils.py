from feedsearch_crawler import search
import tldextract


class FeedUtil:
    url = ""
    feeds = []
    def __init__(self, url):
        self.url = url
        self.__load_feeds()

    def __load_feeds(self):
        self.feeds = search(self.url)
        
    def feed_exists(self):
        True if self.feeds else False
    
    def feeds(self):
        return self.feeds


class URLUtil:
    url = ""

    def get_clean_ur(url):
        clean_url = ""
        return clean_url
