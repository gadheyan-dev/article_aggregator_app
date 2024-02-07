from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from articles.utils.common_utils import convert_urls_to_domain, split_into_visited_and_unvisited
from articles.models.domain import Domain
from articles.serializers.domain import DomainSerializer, DomainUpdateSerialier, CrawledDomainSerializer

class DomainsAPI(APIView):
    
    
    def post(self, request):
        serializer = DomainSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        serializer = DomainUpdateSerialier(data=request.data, many=True, partial=True)
        current_time = datetime.utcnow()
        
        if serializer.is_valid():
            domains = serializer.validated_data

            for updated_domain in domains:
                filter_query = {'url': updated_domain.get('url')}
                update_values = {
                    'set__feeds': updated_domain.get('feeds'),
                    'set__outbound_domains': updated_domain.get('outbound_domains'),
                    'set__is_crawlable': updated_domain.get('is_crawlable'),
                    'set__non_crawlable_reason': updated_domain.get('non_crawlable_reason'),
                    'set__last_crawled_at': updated_domain.get('last_crawled_at', current_time),
                    'set__updated_at': updated_domain.get('updated_at', current_time)
                }

                # Remove None values from the update_values dictionary
                update_values = {k: v for k, v in update_values.items() if v is not None}

                Domain.objects(**filter_query).update_one(upsert=False, **update_values)

            return Response({"message": "Update Successful.", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CheckCrawledDomainAPI(APIView):
    def post(self, request):
        domains = convert_urls_to_domain(request.data['urls'])
        current_time = datetime.utcnow()
        pipeline = [
            {
                '$match': {
                    'url': {'$in': domains}
                }
            },
            {
                '$addFields': {
                    'time_diff_minutes': {
                        '$divide': [
                            {'$subtract': [current_time, '$last_crawled_at']},
                            60000  # milliseconds to minutes conversion factor
                        ]
                    }
                }
            },
            {
                '$set': {
                    'is_crawlable': {
                        '$cond': {
                            'if': {
                                '$and': [
                                    {'$eq': ['$is_crawlable', True]},
                                    {'$lt': ['$time_diff_minutes', '$crawl_delay_in_minutes']}
                                ]
                            },
                            'then': False,
                            'else': '$is_crawlable'
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'url': 1,
                    'is_crawlable': 1,
                    'visited' : True
                }
            }
        ]

        domain_results_cursor = Domain.objects().aggregate(pipeline)
        domain_results = CrawledDomainSerializer(domain_results_cursor, many=True)
        results = split_into_visited_and_unvisited(domains, domain_results.data)
        return Response(results, status=status.HTTP_200_OK)

    
