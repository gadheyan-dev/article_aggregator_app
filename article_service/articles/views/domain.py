from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from articles.utils import get_domain_from_url
from articles.models.domain import Domain
from articles.serializers.domain import DomainSerializer

class DomainAPI(APIView):
    
    def __convert_single_url_to_domain(self, request):
        domain_url = get_domain_from_url(request.data['url'])
        return {"url": domain_url}

    def __get_object(self,domain):
        try:
            return Domain.objects.get(url=domain['url'])
        except Domain.DoesNotExist:
            return Domain(url=domain['url'])
        

    def post(self, request):
        # TODO: Return updated document id
        domain_document = self.__convert_single_url_to_domain(request)
        domain = self.__get_object(domain_document)
        domain.last_crawled_at = datetime.now()
        result = domain.save()
        domain_serializer = DomainSerializer(result)
        return Response(domain_serializer.data, status=status.HTTP_201_CREATED)


class CheckCrawledDomainAPI(APIView):

    def __covert_urls_to_domain(self, request):
        domains = []
        for url in request.data['urls']:
            domains.append(get_domain_from_url(url))
        return domains

    def post(self, request):
        domains = self.__covert_urls_to_domain(request)
        results = Domain.objects.filter(url__in=domains)
        # pipeline = [
        #     {
        #         '$match': {
        #             'url': {'$in': domains}
        #         }
        #     },
        #     {
        #         '$project': {
        #             '_id': 1,
        #             'url': 1,
        #             'is_crawlable': 1,
        #             'last_crawled_at': 1,
        #             'crawl_delay_in_minutes': 1,
        #             'created_at': 1,
        #             'updated_at': 1,
        #             'not_visited': {
        #                 '$cond': {
        #                     'if': {'$eq': ['$url', None]},
        #                     'then': True,
        #                     'else': False
        #                 }
        #             }
        #         }
        #     }
        # ]

        # results = Domain.objects.mongo_aggregate(pipeline)
        domains_results = DomainSerializer(results, many=True)
        return Response(domains_results.data, status=status.HTTP_200_OK)

    
