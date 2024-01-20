from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.settings import Settings

from crawler_app.service.crawler import Crawler
from twisted.internet import reactor



class FindFeed(APIView):
    def post(self, request, format=None):
        feed_url = request.data.get('url')
        feeds = None
        external_domains = None
        if not feed_url:
            return Response({'error': 'Please provide a URL to crawl'}, status=400)
        try:
            crawler = Crawler(feed_url)
            crawler.crawl()
            feeds = crawler.get_feeds()
            external_domains = crawler.get_external_domains()
            print(feeds)
            print(external_domains)
        except Exception as e:
            print("\n\n\n\nException is:")
            import traceback
            print(traceback.format_exc())
            return Response({'error': 'An error occured while crawling...'}, status=400)
            
            
        return Response({'message': 'Crawling started'})