from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from articles.utils import convert_urls_to_domain
from articles.models.domain import Domain
from articles.serializers.domain import DomainSerializer

class DomainsAPI(APIView):
    
    
    def post(self, request):
        serializer = DomainSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
                    'last_crawled_at': 1,
                    'crawl_delay_in_minutes': 1,
                    'created_at': 1,
                    'updated_at': 1,
                }
            }
        ]

        results = Domain.objects().aggregate(pipeline)
        domains_results = DomainSerializer(results, many=True)
        return Response(domains_results.data, status=status.HTTP_200_OK)

    
