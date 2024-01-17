from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from crawler_app.web_crawler.crawler.spiders.find_feeds import FindFeedsSpider



class FindFeed(APIView):
    def post(self, request, format=None):
        feed_url = request.data.get('url')
        if not feed_url:
            return Response({'error': 'Please provide a URL to crawl'}, status=400)
        try:
            settings = Settings()
            settings.setmodule("crawler_app.web_crawler.crawler.settings")

            process = CrawlerProcess(settings)
            process.crawl(FindFeedsSpider, start_url=feed_url)
            process.start()
        except Exception as e:
            print(e)
            return Response({'error': 'An error occured while crawling...'}, status=400)
            

      
        return Response({'message': 'Crawling started'})