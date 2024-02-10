import requests
import json
from django.conf import settings


class ArticleApi:
    """
    ArticleApi class provides methods to interact with an external API for saving articles.

    Attributes:
        None

    Methods:
        save_articles(articles):
            Save articles by sending a POST request to the specified task URL.

    Example:
        Usage of ArticleApi class:
        ```
        articles_data = [
            {
                "title": "Sample Article 1",
                "url": "https://example.com/sample1",
                "authors": [{"name": "John Doe"}],
                "categories": ["Technology"],
                "read_time_in_minutes": 5,
                "publish_date": "2024-02-06T12:00:00Z"
            },
            {
                "title": "\u2018Nothing left\u2019: Indonesia\u2019s tourism industry fears wipeout under tax hike",
                "url": "https://www.aljazeera.com/news/2024/2/4/nothing-left-indonesias-tourism-industry-fears-wipeout-under-tax-hike",
                "categories": [
                    "Technology"
                ],
                "authors": [{"name": "John Doe"}],
                "publish_date": "2024-02-04 23:16:54+00:00",
                "read_time": 5.01,
                "summary": "Plans to introduce 40-75 percent tax rate for entertainment services prompt fierce backlash from businesses.",
                "top_image": "https://www.aljazeera.com/wp-content/uploads/2024/02/AFP__20231118__34423NN__v1__HighRes__IndonesiaLifestyleTourism-1706838152.jpg?resize=1920%2C1440",
                "word_count": 1003
            }
        ]

        # Create an instance of ArticleApi
        article_api = ArticleApi()

        # Save articles using the save_articles method
        response = article_api.save_articles(articles_data)
        print(response)
        ```
    """
    @staticmethod
    def save_articles(articles):
        """
        Save articles by sending a POST request to the specified task URL.

        Args:
            articles (list): A list of articles to be saved.

        Returns:
            dict: JSON response received from the API.

        Example:
            Usage of save_articles method:
            ```
            articles_data =     [
                {
                    "authors": [],
                    "categories": [
                        "News"
                    ],
                    "publish_date": "2024-02-04 23:16:54+00:00",
                    "read_time": 5.01,
                    "summary": "Plans to introduce 40-75 percent tax rate for entertainment services prompt fierce backlash from businesses.",
                    "title": "\u2018Nothing left\u2019: Indonesia\u2019s tourism industry fears wipeout under tax hike",
                    "top_image": "https://www.aljazeera.com/wp-content/uploads/2024/02/AFP__20231118__34423NN__v1__HighRes__IndonesiaLifestyleTourism-1706838152.jpg?resize=1920%2C1440",
                    "url": "https://www.aljazeera.com/news/2024/2/4/nothing-left-indonesias-tourism-industry-fears-wipeout-under-tax-hike?traffic_source=rss",
                    "word_count": 1003
                },
                {
                "authors": [],
                "categories": [
                    "Technology"
                ],
                "publish_date": "2024-02-04 23:16:54+00:00",
                "read_time": 5.01,
                "summary": "Plans to introduce 40-75 percent tax rate for entertainment services prompt fierce backlash from businesses.",
                "title": "\u2018Nothing left\u2019: Indonesia\u2019s tourism industry fears wipeout under tax hike",
                "top_image": "https://www.aljazeera.com/wp-content/uploads/2024/02/AFP__20231118__34423NN__v1__HighRes__IndonesiaLifestyleTourism-1706838152.jpg?resize=1920%2C1440",
                "url": "https://www.aljazeera.com/news/2024/2/4/nothing-left-indonesias-tourism-industry-fears-wipeout-under-tax-hike",
                "word_count": 1003
                }
            ]

            # Create an instance of ArticleApi
            article_api = ArticleApi()

            # Save articles using the save_articles method
            response = article_api.save_articles(articles_data)
            print(response)
            ```
        """
        if not articles:
            return
        taks_url = settings.TASK_URL + 'tasks/save_articles/'
        articles = json.dumps(articles, indent=4, sort_keys=True, default=str)
        response = requests.post(taks_url, json=articles)
        return response.json()
