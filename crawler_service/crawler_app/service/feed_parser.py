import feedparser
from datetime import datetime
from newspaper import Article
from newspaper import Config
from crawler_app.apis.summarizer import SummarizerApi
from crawler_app.utils.common_util import join_lists

class FeedParser():
    def __init__(self, feed_url, domain) -> None:
        self.feed_url = feed_url
        self.domain = domain


    def parse_feed(self):
        # Parse the feed from the provided URL
        feed = feedparser.parse(self.feed_url)
        config = Config()
        config.language = 'en'

        entries = []

        # TODO: Delete this code and add a code to crawl only latest entries
        count = -1
        keywords_request = []
        # Iterate through each entry in the feed
        for entry in feed.entries:
            count += 1
            if count > 5:
                break
            # Extract information from each entry
            article = Article(entry['link'], config=config)
            article.download()
            article.parse()
            # Extract information
            title = entry.title
            if 'author' in entry:  # Check if 'author' tag is present in the entry
                authors = [{'name': entry.author}]
            else:
                authors = []
            publish_date = entry.published or article.publish_date
            publish_date = datetime.strptime(publish_date, '%a, %d %b %Y %H:%M:%S %z')
            word_count = len(article.text.split())
            read_time = round(word_count / 200, 2)  # Assuming an average reading speed of 200 words per minute
            categories = entry.get('tags', [])
            categories = [c["term"] for c in categories]
            # Extract the top image
            top_image = article.top_image

            # Save the main content as a summary (teaser)
            summary = article.meta_description
            # Add in try catch
            # TODO: Make it more efficient by giving only a single request
            keywords_request.append({"url":article.url,"text":article.text})
            # Store the information in a dictionary
            article_info = {
                'url': article.url,
                'title':title,
                'authors': authors,
                'source': self.feed_url,
                'domain': self.domain,
                'word_count': word_count,
                'read_time_in_minutes': read_time,
                'categories': categories,
                'top_image': top_image,
                'summary': summary,
                'publish_date': publish_date.isoformat(),
            }

            entries.append(article_info)
        
        keywords = SummarizerApi.extract_keywords(keywords_request, many=True)
        entries = join_lists(entries,keywords )
        return entries
