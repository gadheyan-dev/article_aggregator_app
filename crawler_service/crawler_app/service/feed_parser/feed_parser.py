import feedparser

class FeedParser():
    def __init__(self, feed_url) -> None:
        self.feed_url = feed_url


    def parse_feed(self):
        # Parse the feed from the provided URL
        feed = feedparser.parse(url)

        entries = []

        # Iterate through each entry in the feed
        for entry in feed.entries:
            # Extract information from each entry
            title = entry.title
            url = entry.link
            authors = [author.name for author in entry.authors] if 'authors' in entry else []
            summary = entry.summary if 'summary' in entry else ''
            publish_date = entry.published_parsed if 'published_parsed' in entry else None
            word_count = len(entry.summary.split()) if 'summary' in entry else 0
            read_time = int(word_count / 200) + 1  # Assuming an average reading speed of 200 words per minute
            categories = entry.get('tags', [])

            # Create a dictionary with the extracted information
            entry_info = {
                'title': title,
                'url': url,
                'authors': authors,
                'summary_of_article': summary,
                'publish_date': publish_date,
                'word_count': word_count,
                'read_time': read_time,
                'categories': categories
            }

            # Append the dictionary to the list of entries
            entries.append(entry_info)

        return entries
