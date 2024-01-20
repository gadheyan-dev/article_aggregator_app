from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from articles.utils import get_domain_from_url
from articles.models.domain import Domain

class DomainAPI(APIView):
    
    def get_object(self, request):
        # TODO: extract domain from url
        domain_url = request.data['url']
        domain_url = get_domain_from_url(domain_url)
        return {'url', domain_url}

    def post(self, request):
        domain_document = self.get_object(request)
        print(type(domain_document))
        # domain_obj = Domain.objects.mongo_find(domain_document)
        return Response(domain_obj, status=status.HTTP_201_CREATED)


    
