import requests
from django.conf import settings
import json 
from django.core.serializers.json import DjangoJSONEncoder


class TasksApi:

    @staticmethod
    def add_task_to_save_articles(article_list):
        if not article_list:
            return
        taks_url = settings.TASK_URL + 'tasks/save_articles/'
        with open('example.json', 'w') as file:
            # Write data to the file
            file.write(json.dumps(article_list, indent=4, sort_keys=True, cls=DjangoJSONEncoder))
        for articles_obj in article_list:
            articles = articles_obj["articles"]
            # articles = json.dumps(articles, indent=4, sort_keys=True, cls=DjangoJSONEncoder)
            response = requests.post(taks_url, json=articles)
        return response.json()