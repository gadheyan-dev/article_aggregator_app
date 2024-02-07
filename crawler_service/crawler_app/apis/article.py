import requests
import json
from django.conf import settings

class ArticleApi:
    @staticmethod
    def save_articles(articles):
        if not articles:
            return
        taks_url = settings.TASK_URL + 'tasks/save_articles/'
        articles=json.dumps(articles, indent=4, sort_keys=True, default=str)

        # Open a file in write mode ('w')
        with open('example.json', 'w') as file:
            # Write data to the file
            file.write(articles)

        response = requests.post(taks_url, json=articles)
        return response.json()