import requests
from django.conf import settings

class TasksApi:

    @staticmethod
    def add_task_to_save_articles(article_list):
        if not article_list:
            return
        taks_url = settings.TASK_URL + 'tasks/save_articles/'
        for articles_obj in article_list:
            articles = articles_obj["articles"]
            response = requests.post(taks_url, json=articles)
        return response.json()