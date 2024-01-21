from django.shortcuts import render


from articles.models.article import Article
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articles.serializers.article import ArticleSerializer
from articles.utils import parse_json


class ArticleAPI(APIView):
    def __get_object(self, url):
        try:
            return Article.objects.get(url=url)
        except Article.DoesNotExist:
            return Article(url=url)

    def post(self, request):
        url = self.request.data.get('url')
        instance = Article.objects.filter(url=url).first()

        if instance:
            serializer = ArticleSerializer(instance, data=request.data)
        else:
            serializer = ArticleSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


        
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    
