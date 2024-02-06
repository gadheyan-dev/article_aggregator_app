from urllib import robotparser

class CrawlerRobotParserUtil():
    def __init__(self, url="", agent = "RSSFeedBot") -> None:
        self.base_url = url
        self.agent = agent
        self.rp = robotparser.RobotFileParser()
        self.rp.set_url(self.base_url)
        self.rp.read()
    
    def crawl_allowed(self):
        return self.rp.can_fetch(self.agent, self.base_url)