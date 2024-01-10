from datetime import datetime
from articles.models.article import Article
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articles.serializers.article import ArticleSerializer


class ArticleListAPI(APIView):
    def post(self, request):
        serializer = ArticleSerializer(data=request.data, many=True)
        current_time = datetime.utcnow()
        if serializer.is_valid():
            articles = serializer.validated_data
            for updated_article in articles:
                filter_query = {'url': updated_article.get('url')}
                update_values = {
                    'set__title': updated_article.get('title'),
                    'set__url': updated_article.get('url'),
                    'set__top_image': updated_article.get('top_image'),
                    'set__authors': updated_article.get('authors'),
                    'set__summary': updated_article.get('summary'),
                    'set__publish_date': updated_article.get('publish_date'),
                    'set__updated_at': updated_article.get('updated_at', current_time)
                }

                # Remove None values from the update_values dictionary
                update_values = {k: v for k, v in update_values.items() if v is not None}

                Article.objects(**filter_query).update_one(upsert=True, **update_values)

            return Response({"message": "Update Successful.", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    
