import sys,os
sys.path.append(os.getcwd())
import time
import requests
from django.conf import settings
from celery import shared_task
# from web_crawler.crawler.spiders.find_feeds import FindFeedsSpider
# from scrapy.crawler import CrawlerProcess,CrawlerRunner
# from scrapy.settings import Settings
# from twisted.internet import reactor


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


# @shared_task
# def find_rss_feeds_from_url(data):

#     start_url = data['start_url']
#     if not start_url:
#             return {'error': 'Please provide a URL to crawl'}
#     try:
#         settings = Settings()
#         settings.setmodule("web_crawler.crawler.settings")
#         # process = CrawlerProcess(settings)
#         # process.crawl(FindFeedsSpider, start_url=start_url)
#         # print("Crawling is Starting:\n\n\n\n")
#         # process.start()
#         # print("Crawling Started:\n\n\n\n")
#         runner = CrawlerRunner(settings)
#         runner.crawl(FindFeedsSpider, start_url=start_url)
#         # Start the reactor to run the spider
#         d = runner.join()
#         d.addBoth(lambda _: reactor.stop())
#         reactor.run()
#     except Exception as e:
#         print("\n\n\n\nException is:")
#         import traceback
#         print(traceback.format_exc())
