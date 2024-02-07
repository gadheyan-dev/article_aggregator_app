from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crawler_app.service.crawler import Crawler
from crawler_app.service.feed_parser import FeedParser
from crawler_app.apis.domain import DomainApi
from crawler_app.apis.tasks import TasksApi


class FindFeed(APIView):
    def post(self, request):
        feed_urls = request.data
        if not feed_urls:
            return Response({'error': 'Please provide atleast 1 URL to crawl'}, status=400)
        try:
            visited_and_unvisited_domains = DomainApi.fetch_crawled_domains(feed_urls)
            crawled_domains = self.crawl_domains(visited_and_unvisited_domains)

            DomainApi.save_domains(crawled_domains)
            DomainApi.save_outbound_domains(crawled_domains)
            articles_list = self.parse_feeds(crawled_domains)
            TasksApi.add_task_to_save_articles(articles_list)
        except Exception as e:
            print("\n\n\n\nException is:")
            import traceback
            print(traceback.format_exc())
            return Response({'error': 'An error occured while crawling...'}, status=400)
        return Response({'domains': crawled_domains, 'articles': articles_list}, status=status.HTTP_200_OK)


    def crawl_domains(self, domains):
        for domain in domains:
            try:
                # print("Url Is:")
                # print(url)
                url = domain['url']
                crawler = Crawler(url)
                crawler.crawl()
                # feeds[url] = {'feeds': crawler.get_feeds(), 'outbound_domains': crawler.get_outbound_domains(), 'crawlable':True}
                domain['feeds'] = crawler.get_feeds()
                domain['outbound_domains'] = crawler.get_outbound_domains()

            except Exception as e:
                domain['feeds'] = []
                domain['outbound_domains'] = []
                # print("URL Is:" + url)
                # print("\n\n\n\nException is:")
                # import traceback
                # print(traceback.format_exc())
        
        return domains
    

    def parse_feeds(self, feeds):
        articles = []
        if not feeds:
            # Raise Exception
            return []
        try:
            for feed in feeds:
                for feed_url in feed['feeds']:
                    feed_obj = FeedParser(feed_url)
                    feed_data = feed_obj.parse_feed()
                    articles.append({'feed_url':feed_url,'articles':feed_data})
                
        except Exception as e:
            print("\n\n\n\nException is:")
            import traceback
            print(traceback.format_exc())
        
        return articles
    
    