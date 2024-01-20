from django.shortcuts import render


from ..models.aritcle import Article
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import ArticleSerializer
from articles.utils import parse_json


class ArticleAPI(APIView):
    
    def post(self, request):
        # serializer = ArticleSerializer(data=request.data)
        
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        article = Article(
            title = request.data['title']
        )
        article.save()
        return Response(request.data, status=status.HTTP_201_CREATED)


        
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    
