import requests
import json
from django.conf import settings

class SummarizerApi:
    @staticmethod
    def extract_keywords(articles, many=False):
        if not articles:
            return
        if not many:
            articles = [articles]
        url = settings.SUMMARIZER_URL + 'keywords/extract/'
        # articles=json.dumps(articles, indent=4, sort_keys=True, default=str)

        # # Open a file in write mode ('w')
        # with open('example.json', 'w') as file:
        #     # Write data to the file
        #     file.write(articles)

        response = requests.post(url, json=articles)
        response = response.json()
        if response and not many:
            response = response[0]
        return response