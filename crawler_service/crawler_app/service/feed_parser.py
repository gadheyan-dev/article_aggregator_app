import feedparser
from newspaper import Article
from newspaper import Config

class FeedParser():
    def __init__(self, feed_url) -> None:
        self.feed_url = feed_url


    def parse_feed(self):
        # Parse the feed from the provided URL
        feed = feedparser.parse(self.feed_url)
        config = Config()
        config.language = 'en'

        entries = []

        # TODO: Delete this code
        count = -1
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
            authors = article.authors
            publish_date = article.publish_date
            word_count = len(article.text.split())
            read_time = word_count / 200  # Assuming an average reading speed of 200 words per minute
            categories = entry.get('tags', [])


            # Extract the top image
            top_image = article.top_image

            # Save the main content as a summary (teaser)
            summary = article.meta_description

            # Store the information in a dictionary
            article_info = {
                'url': article.url,
                'authors': authors,
                'publish_date': publish_date,
                'word_count': word_count,
                'read_time': read_time,
                'categories': categories,
                'top_image': top_image,
                'summary': summary
            }

            entries.append(article_info)

        return entries
