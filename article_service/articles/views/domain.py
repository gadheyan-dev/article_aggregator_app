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
        serializer = DomainUpdateSerialier(data=request.data, many=True)
        current_time = datetime.utcnow()

        if serializer.is_valid():
            domains = serializer.validated_data

            for updated_domain in domains:
                filter_query = {'url': updated_domain.get('url')}
                update_values = {
                    'set__feeds': updated_domain.get('feeds'),
                    'set__outbound_domains': updated_domain.get('outbound_domains'),
                    'set__inbound_domains': updated_domain.get('inbound_domains'),
                    'set__is_crawlable': updated_domain.get('is_crawlable'),
                    'set__non_crawlable_reason': updated_domain.get('non_crawlable_reason'),
                    'set__last_crawled_at': updated_domain.get('last_crawled_at', current_time),
                    'set__updated_at': updated_domain.get('updated_at', current_time)
                }

                Domain.objects(
                    **filter_query).update_one(upsert=False, **update_values)

            return Response({"message": "Update Successful.", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = DomainUpdateSerialier(
            data=request.data, many=True, partial=True)
        current_time = datetime.utcnow()

        if serializer.is_valid():
            domains = serializer.validated_data

            for updated_domain in domains:
                filter_query = {'url': updated_domain.get('url')}
                update_values = {
                    'set__feeds': updated_domain.get('feeds', None),
                    'push__inbound_domains__each': updated_domain.get('outbound_domains', []),
                    'push__inbound_domains__each': updated_domain.get('inbound_domains', []),
                    'set__is_crawlable': updated_domain.get('is_crawlable', None),
                    'set__non_crawlable_reason': updated_domain.get('non_crawlable_reason', None),
                    'set__last_crawled_at': updated_domain.get('last_crawled_at', current_time),
                    'set__updated_at': updated_domain.get('updated_at', current_time)
                }

                update_values = {k: v for k,
                                 v in update_values.items() if v is not None}

                Domain.objects(
                    **filter_query).update_one(upsert=False, **update_values)

            return Response({"message": "Update Successful.", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckCrawledDomainAPI(APIView):
    def post(self, request):
        """
        API endpoint for checking the crawlability status of domains.

        This endpoint takes a list of URLs, extracts their domains, and checks their crawlability status.
        The crawlability is determined based on the last crawled time and the specified crawl delay for each domain.

        Parameters:
            - request (HttpRequest): The HTTP request object containing a list of URLs.

        Returns:
            - Response: A JSON response containing the crawlability status of each domain.

                - Success (HTTP 200 OK):
                    {
                        "visited": [
                            {
                                "_id": "domain_id",
                                "url": "https://example.com",
                                "is_crawlable": False,
                                "visited": True
                            },
                            ...
                        ],
                        "unvisited": [
                            {
                                "url": "https://newdomain.com",
                                "is_crawlable": True,
                                "visited": True
                            },
                            ...
                        ]
                    }

                - Failure (HTTP 400 Bad Request):
                    {
                        "success": False,
                        "errors": {"urls": "Invalid or empty list of URLs"}
                    }
        """
        # TODO: Currently this function is reduntant, since domains are already cleaned when receiving.. May be useful when request received from a different channel.
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
                            60000
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
                                    {'$lt': ['$time_diff_minutes',
                                             '$crawl_delay_in_minutes']}
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
                    'visited': True
                }
            }
        ]

        domain_results_cursor = Domain.objects().aggregate(pipeline)
        domain_results = CrawledDomainSerializer(
            domain_results_cursor, many=True)
        results = split_into_visited_and_unvisited(
            domains, domain_results.data)
        return Response(results, status=status.HTTP_200_OK)
