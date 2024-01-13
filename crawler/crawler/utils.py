from feedsearch_crawler import search


class Util:
    url = ""
    feeds = []
    def __init__(self, url):
        self.url = url
        load_feeds()

    def load_feeds():
        self.feeds = search(self.url)

    def feed_exists(self):
        True if self.feeds else False
    
    def feeds(self):
        return self.feeds


