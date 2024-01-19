from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.settings import Settings

from web_crawler.crawler.spiders.find_feeds import FindFeedsSpider
from twisted.internet import reactor



class FindFeed(APIView):
    def post(self, request, format=None):
        feed_url = request.data.get('url')
        if not feed_url:
            return Response({'error': 'Please provide a URL to crawl'}, status=400)
        try:
            settings = Settings()
            settings.setmodule("web_crawler.crawler.settings")
            # runner = CrawlerRunner(settings)
            # runner.crawl(FindFeedsSpider, start_url=feed_url)
            # # Start the reactor to run the spider
            # d = runner.join()
            # d.addBoth(lambda _: reactor.stop())
            # reactor.run()
            process = CrawlerProcess(settings)
            process.crawl(FindFeedsSpider, start_url=feed_url)
            print("Crawling is Starting:\n\n\n\n")
            process.start()
            print("Crawling Started:\n\n\n\n")
        except Exception as e:
            print("\n\n\n\nException is:")
            print(str(e))
            print(e.__class__)
            
            return Response({'error': 'An error occured while crawling...'}, status=400)
            

      
        return Response({'message': 'Crawling started'})