from datetime import datetime
from articles.models.article import Article
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articles.serializers.article import ArticleSerializer


class ArticleListAPI(APIView):

    def post(self, request):
        """
        API endpoint for creating or updating multiple articles.

        This endpoint allows the creation or update of multiple articles in the database.
        Articles are identified by their URLs, and existing articles will be updated if
        their URLs match those provided in the request data. If an article with a new URL
        is provided, a new article will be created.

        Parameters:
            - request (HttpRequest): The HTTP request object containing data for articles.

        Returns:
            - Response: A JSON response indicating the success or failure of the operation.

                - Success (HTTP 200 OK):
                    {
                        "success": True,
                        "message": "Articles Created/Updated Successfully.",
                        "data": [serialized_articles]
                    }

                - Failure (HTTP 400 Bad Request):
                    {
                        "success": False,
                        "errors": [serializer_errors]
                    }

        Notes:
            - The request data should be a list of articles serialized using the
            ArticleSerializer. Each article is identified by its URL.

        Example:
            An example request body:
            [
                {
                    "title": "Sample Article 1",
                    "url": "https://example.com/sample1",
                    "authors": [{"name": "John Doe"}],
                    "categories": ["Technology"],
                    "read_time_in_minutes": 5,
                    "publish_date": "2024-02-06T12:00:00Z"
                },
                {
                    "title": "Sample Article 2",
                    "url": "https://example.com/sample2",
                    "authors": [{"name": "Jane Doe"}],
                    "categories": ["Science"],
                    "read_time_in_minutes": 8,
                    "publish_date": "2024-02-06T13:30:00Z"
                }
            ]
        """
        serializer = ArticleSerializer(data=request.data, many=True)
        current_time = datetime.utcnow()
        if serializer.is_valid():
            articles = serializer.validated_data
            for updated_article in articles:

                filter_query = {'url': updated_article.get('url')}
                update_values = {
                    'set__title': updated_article.get('title'),
                    'set__url': updated_article.get('url'),
                    'set__source': updated_article.get('source'),
                    'set__top_image': updated_article.get('top_image'),
                    'set__authors': updated_article.get('authors'),
                    'set__summary': updated_article.get('summary'),
                    'set__read_time_in_minutes': updated_article.get('read_time_in_minutes'),
                    'set__word_count': updated_article.get('word_count'),
                    'set__categories': updated_article.get('categories'),
                    'set__publish_date': updated_article.get('publish_date'),
                    'set__updated_at': updated_article.get('updated_at', current_time)
                }
                update_values = {k: v for k,
                                 v in update_values.items() if v is not None}
                Article.objects(
                    **filter_query).update_one(upsert=True, **update_values)
            return Response(data={"success": True, "message": "Articles Created/Updated Successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(data={"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
