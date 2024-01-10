import requests
import json
from django.conf import settings

class ArticleApi:
    @staticmethod
    def save_articles(articles):
        if not articles:
            return
        taks_url = settings.TASK_URL + 'tasks/save_articles/'
        response = requests.post(taks_url, json=json.dumps(articles, indent=4, sort_keys=True, default=str))
        return response.json()