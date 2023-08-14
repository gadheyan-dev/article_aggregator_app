from rest_framework.views import APIView
from rest_framework.response import Response
from .services.summarizer import ArticleSummarizer
from .serializers import ArticleSerializer
from rest_framework import status

class ArticleList(APIView):
    
    def post(self, request, format=None):
        data = request.data
        article_obj = ArticleSummarizer(data['url'])
        article = article_obj.get_article()
        serializer = ArticleSerializer(article)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


