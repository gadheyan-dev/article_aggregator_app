import requests
from django.conf import settings

class TasksApi:

    @staticmethod
    def add_task_to_save_articles(articles_list):
        if not articles_list:
            return
        taks_url = settings.TASK_URL + 'tasks/save_articles/'
        # articles=json.dumps(articles, indent=4, sort_keys=True, default=str)

        # Open a file in write mode ('w')
        with open('example.json', 'w') as file:
            # Write data to the file
            file.write(articles_list)
        for articles_obj in articles_list:
            response = requests.post(taks_url, json=articles_obj.art)
        return response.json()