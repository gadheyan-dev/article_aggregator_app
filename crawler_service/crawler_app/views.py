from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from crawler_app.service.crawler import Crawler
from crawler_app.service.feed_parser import FeedParser
from crawler_app.apis.domain import DomainApi
from crawler_app.apis.tasks import TasksApi
from crawler_app.constants import NOT_REACHABLE, NOT_CRAWLABLE
from crawler_exceptions.exceptions import WebsiteNotReachableException, CrawlNotAllowedException
import logging

logger = logging.getLogger(__name__)




class FindFeed(APIView):
    def post(self, request):
        feed_urls = request.data
        if not feed_urls:
            return Response({'error': 'Please provide atleast 1 URL to crawl'}, status=400)
        try:
            visited_and_unvisited_domains = DomainApi.fetch_crawled_domains(
                feed_urls)
            logger.info(visited_and_unvisited_domains)
            crawled_domains = self.crawl_domains(visited_and_unvisited_domains)
            # TODO: check for social media before saving
            DomainApi.save_domains(crawled_domains)
            DomainApi.save_outbound_domains(crawled_domains)
            articles_list = self.parse_feeds(crawled_domains)
            TasksApi.add_task_to_save_articles(articles_list)
        except Exception as e:
            logger.exception("Exception Occured:\n %s", e)
            return Response({'error': 'An error occured while crawling...'}, status=400)
        return Response({'domains': crawled_domains, 'articles': articles_list}, status=status.HTTP_200_OK)

    def crawl_domains(self, domains):
        for domain in domains:
            try:
                url = domain['url']
                crawler = Crawler(url)
                crawler.crawl()
                domain['feeds'] = crawler.get_feeds()
                domain['outbound_domains'] = crawler.get_outgoing_domains()

            except (WebsiteNotReachableException, CrawlNotAllowedException) as e:
                domain['feeds'] = []
                domain['outbound_domains'] = []
                domain['is_crawlable'] = False
                # TODO:
                 # Log error
                if isinstance(e, WebsiteNotReachableException):
                    domain['non_crawlable_reason'] = NOT_REACHABLE
                    logger.exception("Exception Occured:\n %s", e)
                if isinstance(e, CrawlNotAllowedException):
                    domain['non_crawlable_reason'] = NOT_CRAWLABLE
                    logger.exception("Exception Occured:\n %s", e)
                

        return domains

    def parse_feeds(self, domains):
        articles = []
        if not domains:
            # Raise Exception
            return []
        try:
            for domain in domains:

                for feed_url in domain['feeds']:
                    feed_obj = FeedParser(feed_url, domain['url'])
                    feed_data = feed_obj.parse_feed()
                    articles.append(
                        {'feed_url': feed_url, 'articles': feed_data})

        except Exception as e:
            logger.exception("Exception Occured:\n %s", e)

        return articles
