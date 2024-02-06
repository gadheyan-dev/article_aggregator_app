from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crawler_app.service.crawler import Crawler
from crawler_service.crawler_app.service.feed_parser import FeedParser
from crawler_service.crawler_app.apis.articles.domain import DomainApi

class ParseFeed(APIView):
    def post(self, request):
        feed_url = request.data.get('url')
        feeds = None
        if not feed_url:
            return Response({'error': 'Please a valid Feed URL'}, status=400)
        try:
            feed_obj = FeedParser(feed_url)
            feeds = feed_obj.parse_feed()
            print(feeds)
            return Response(feeds, status=200)
        except Exception as e:
            print("\n\n\n\nException is:")
            import traceback
            print(traceback.format_exc())
            return Response({'error': 'An error occured while parsing...'}, status=400)
            
            


class FindFeed(APIView):
    def post(self, request):
        feed_urls = request.data
        feeds = None
        outbound_domains = None
        if not feed_urls:
            return Response({'error': 'Please provide atleast 1 URL to crawl'}, status=400)
        try:
            visited_and_unvisited_domains = DomainApi.fetch_crawled_domains(feed_urls)
            crawled_domains = self.crawl_domains(visited_and_unvisited_domains)
            DomainApi.save_domains(crawled_domains)
            # DomainApi.crawl_domains(visited_and_unvisited_domains)
            # DomainApi.parse_feeds(feeds)
        except Exception as e:
            print("\n\n\n\nException is:")
            import traceback
            print(traceback.format_exc())
            return Response({'error': 'An error occured while crawling...'}, status=400)
        return Response({'feeds': feeds, "outbound_domains":outbound_domains}, status=status.HTTP_200_OK)


    def crawl_domains(self, domains):
        feeds = {}
        outbound_domains = set()
        for url in domains:
            try:
                crawler = Crawler(url)
                crawler.crawl()
                feeds[url] = {'feeds': crawler.get_feeds(), 'outbound_domains': crawler.get_outbound_domains(), 'crawlable':True}
                outbound_domains = outbound_domains.union(crawler.get_outbound_domains())
            except Exception as e:
                feeds[url] = {'feeds':[],
                              'crawlable':False}
                # print("URL Is:" + url)
                # print("\n\n\n\nException is:")
                # import traceback
                # print(traceback.format_exc())
        
        return feeds
    
    