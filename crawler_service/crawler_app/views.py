from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crawler_app.service.crawler import Crawler
from crawler_app.service.feed_parser.feed_parser import FeedParser
from crawler_app.service.utils.domain_util import DomainUtil

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
        feed_urls = request.data.get('urls')
        feeds = None
        external_domains = None
        if not feed_urls:
            return Response({'error': 'Please provide atleast 1 URL to crawl'}, status=400)
        try:
            feeds, external_domains = self.__get_feeds_and_domains(feed_urls)
            domains_to_crawl = DomainUtil.get_domain_to_crawl(external_domains)
            print(feeds)
            print(domains_to_crawl)
            # DomainUtil.add_to_tasks(domains_to_crawl)
        except Exception as e:
            print("\n\n\n\nException is:")
            import traceback
            print(traceback.format_exc())
            return Response({'error': 'An error occured while crawling...'}, status=400)
        return Response({'message': 'Crawling started'})


    def __get_feeds_and_domains(self, feed_urls):
        feeds = set()
        external_domains = set()
        for url in feed_urls:
            try:
                crawler = Crawler(url)
                crawler.crawl()
                feeds.union(crawler.get_feeds())
                external_domains.union(crawler.get_external_domains())
            except Exception as e:
                print("URL Is:" + url)
                print("\n\n\n\nException is:")
                import traceback
                print(traceback.format_exc())
        
        return feeds, external_domains
    
    