
from celery import shared_task
import time
import requests
from django.conf import settings
from .utils import convert_to_json

@shared_task
def summarize_and_save(data):
    summarizer_url = settings.SUMMARIZER_URL
    summarizer_url = summarizer_url + "summarize/"

    article_url = settings.ARTICLE_URL
    article_url = article_url + "articles/"

    try:
        response = requests.post(summarizer_url, json=data)
        summary = response.json()
        respone_from_article = requests.post(article_url, json=summary)
        # print("\n\n\n\n\nResponse Ar:\n")
        # print(respone_from_article.content)
    except requests.exceptions.RequestException as e:
        # Log error
        print("error: ", e)

