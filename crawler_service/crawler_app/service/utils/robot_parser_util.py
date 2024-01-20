from urllib import robotparser

AGENT = "RSSFeedBot"
url = "https://edition.cnn.com/"
rp = robotparser.RobotFileParser()
rp.set_url(url)
rp.read()
print(rp.can_fetch(AGENT,url))


class CrawlerRobotParserUtil():
    def __init__(self, url="", agent = "RSSFeedBot") -> None:
        self.base_url = url
        self.agent = agent
        self.rp = robotparser.RobotFileParser()
        rp.set_url(self.base_url)
        rp.read()
    
    def crawl_allowed(self):
        return rp.can_fetch(self.agent, self.base_url)