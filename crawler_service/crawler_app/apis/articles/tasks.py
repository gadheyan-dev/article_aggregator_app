import requests
from django.conf import settings

class TasksApi:

    @staticmethod
    def add_task_to_save_articles(articles):
        article_url = settings.TASK_URL + 'tasks/save_articles/'
        response = requests.post(article_url, json=articles)
        return response
    
 