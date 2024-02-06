from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from pymongo import UpdateOne

from articles.utils.common_utils import convert_urls_to_domain, split_into_visited_and_unvisited
from articles.models.domain import Domain
from articles.serializers.domain import DomainSerializer, CrawledDomainSerializer

class DomainsAPI(APIView):
    
    
    def post(self, request):
        serializer = DomainSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        domains_data = request.data
        # serializer = DomainSerializer(data=domains_data, partial=True, many=True)
        
        # if serializer.is_valid():
        domain_list = []
        for domain_data in domains_data:
            url =  convert_urls_to_domain(domain_data['url'], many=False)
            domain_list.append(url)
        for domain_data in domains_data:
            # url =  convert_urls_to_domain(domain_data['urls'], many=False)
            domain_instance = Domain.objects.filter(url=domain_data['url']).first()
            update_dict = {}
            if domain_instance:
                for key, value in domain_data.items():
                    update_dict[key] = value
                # domain_instance.update()
                bulk_operations.append(
                    UpdateOne(
                        {"url": domain_instance['url']},
                        {"$set": update_dict}
                    )
                )
            results = Domain.objects._get_collection().bulk_write(bulk_operations)
            return Response({"message":f"{len(results)} domains updated successfully"}, status=status.HTTP_200_OK)
       
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)



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

    
