from articles.models.article import Article
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articles.serializers.article import ArticleSerializer


class ArticleListAPI(APIView):
    # def __get_object(self, url):
    #     try:
    #         return Article.objects.get(url=url)
    #     except Article.DoesNotExist:
    #         return Article(url=url)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    
