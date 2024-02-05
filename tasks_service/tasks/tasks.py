import sys,os
sys.path.append(os.getcwd())
import time
import requests
from django.conf import settings
from celery import shared_task


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
    except requests.exceptions.RequestException as e:
        # Log error
        print("error: ", e)


@shared_task
def find_rss_feeds_from_url(data):
    crawler_url = settings.CRAWLER_URL + '/crawl/find_feeds/'
    start_url = data['url']
    if not start_url:
            return {'error': 'Please provide a URL to crawl'}
    try:
        response = requests.post(crawler_url, json=data)
    except requests.exceptions.RequestException as e:
        # Log error
        print("error: ", e)


@shared_task
def parse_feeds(data):
    crawler_url = settings.CRAWLER_URL + '/crawl/parse_feeds/'
    feeds = data['feeds']
    if not feeds:
            return {'error': 'Please provide atleast 1 URL to crawl'}
    try:
        response = requests.post(crawler_url, json=data)
        # TODO: LOG Response
    except requests.exceptions.RequestException as e:
        # Log error
        print("error: ", e)
