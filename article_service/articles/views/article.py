from datetime import datetime
from articles.models.article import Article
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articles.serializers.article import ArticleSerializer, ArticlePipelineSerializer
from mongoengine import Q


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
                    'set__domain': updated_article.get('domain'),
                    'set__keywords': updated_article.get('keywords'),
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
        # print(serializer.errors)
        return Response(data={"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        keyword = request.data.get("keyword", "technology")
    #     pipeline = [
    #         {"$unwind": "$keywords"},
    #         {"$match": {"keywords.text": {"$regex": f'{keyword}', "$options": 'i'}}},
    #         {"$addFields": {"exact": {"$eq": ["$keywords.text", keyword]}}},
    #         {"$addFields": {"read_time_score": {
    #             "$switch": {
    #                 "branches": [
    #                     {"case": {
    #                         "$lt": ["$read_time_in_minutes", 1]}, "then": 2},
    #                     {"case": {
    #                         "$lte": ["$read_time_in_minutes", 2]}, "then": 8},
    #                     {"case": {
    #                         "$lte": ["$read_time_in_minutes", 10]}, "then": 10},
    #                     {"case": {
    #                         "$lte": ["$read_time_in_minutes", 20]}, "then": 8},
    #                     {"case": {
    #                         "$lte": ["$read_time_in_minutes", 50]}, "then": 6},
    #                     {"case": {
    #                         "$lte": ["$read_time_in_minutes", 90]}, "then": 4},
    #                     {"case": {
    #                         "$gt": ["$read_time_in_minutes", 90]}, "then": 2}
    #                 ],
    #                 "default": 0
    #             }
    #         }}},
    #   {"$group": {
    #     "_id": "$_id",  # Group by the article id
    #     "url": {"$first": "$url"},  # Use $first to get the url
    #     "title": {"$first": "$title"},
    #     "top_image": {"$first": "$top_image"},
    #     "summary": {"$first": "$summary"},
    #     "published_date": {"$first": "$publish_date"},
    #     "keywords": {"$push": "$keywords"},  # Use $push for arrays
    #     "exact": {"$first": "$exact"},
    #     "read_time_score": {"$first": "$read_time_score"},
    # }},

    #         {"$project": {"_id": 1, "url": 1, "title": 1, "top_image": 1, "summary": 1,"published_date":1,
    #                       "keywords": 1, "exact": 1, "read_time_score": 1}}
    #     ]
        pipeline = [
            {"$unwind": "$keywords"},
            {"$match": {"keywords.text": {"$regex": f'{keyword}', "$options": 'i'}}},
            {"$addFields": {"keyword_score": "$keywords.score"}},
            {"$addFields": {"exact": {"$eq": ["$keywords.text", keyword]}}},
            {"$addFields": {"title_score": {
                "$cond": {
                    "if": {"$regexMatch": {"input": "$title", "regex": f'{keyword}', "options": "i"}},
                    "then": 15,
                    "else": 0
                }
            }}},
            {"$addFields": {"category_score": {
                "$cond": {
                    "if": {"$in": [keyword, "$categories"]},
                    "then": 10,
                    "else": 0
                }
            }}},
            {"$addFields": {"read_time_score": {
                "$switch": {
                    "branches": [
                        {"case": {
                            "$lt": ["$read_time_in_minutes", 1]}, "then": 2},
                        {"case": {
                            "$lte": ["$read_time_in_minutes", 2]}, "then": 8},
                        {"case": {
                            "$lte": ["$read_time_in_minutes", 10]}, "then": 10},
                        {"case": {
                            "$lte": ["$read_time_in_minutes", 20]}, "then": 8},
                        {"case": {
                            "$lte": ["$read_time_in_minutes", 50]}, "then": 6},
                        {"case": {
                            "$lte": ["$read_time_in_minutes", 90]}, "then": 4},
                        {"case": {
                            "$gt": ["$read_time_in_minutes", 90]}, "then": 2}
                    ],
                    "default": 0
                }
            }}},
            {"$addFields": {"recency_score": {
                "$let": {
                    "vars": {
                        "diffInDays": {
                            "$divide": [
                                {"$subtract": [
                                    datetime.utcnow(), "$publish_date"]},
                                86400000  # milliseconds in a day
                            ]
                        }
                    },
                    "in": {
                        "$cond": {
                            "if": {"$lt": ["$$diffInDays", 5]},
                            "then": 10,
                            "else": {
                                "$switch": {
                                    "branches": [
                                        {"case": {
                                            "$lt": ["$$diffInDays", 30]}, "then": 9},
                                        {"case": {
                                            "$lt": ["$$diffInDays", 90]}, "then": 8},
                                        {"case": {
                                            "$lt": ["$$diffInDays", 180]}, "then": 7},
                                        {"case": {
                                            "$lt": ["$$diffInDays", 365]}, "then": 6},
                                        {"case": {
                                            "$lt": ["$$diffInDays", 730]}, "then": 4},
                                    ],
                                    "default": 2
                                }
                            }
                        }
                    }
                }
            }}},
            {"$addFields": {"total_score": {
                "$add": ["$title_score", "$category_score", "$read_time_score", "$recency_score", "$keyword_score"]
            }}},
            {"$group": {
                "_id": "$_id",  # Group by the article id
                "url": {"$first": "$url"},  # Use $first to get the url
                "title": {"$first": "$title"},
                "top_image": {"$first": "$top_image"},
                "summary": {"$first": "$summary"},
                "published_date": {"$first": "$publish_date"},
                "keywords": {"$push": "$keywords"},  # Use $push for arrays
                "exact": {"$first": "$exact"},
                "title_score": {"$first": "$title_score"},
                "category_score": {"$first": "$category_score"},
                "read_time_score": {"$first": "$read_time_score"},
                "recency_score": {"$first": "$recency_score"},
                "keyword_score": {"$first": "$keyword_score"},
                "total_score": {"$first": "$total_score"},
            }},
            {"$project": {"_id": 1, "url": 1, "title": 1, "top_image": 1, "summary": 1, "published_date": 1,
                          "keywords": 1, "exact": 1, 'title_score': 1, 'category_score': 1, 'read_time_score': 1, 'recency_score': 1, "total_score": 1, 'keyword_score': 1}},
            { "$sort": { "total_score": -1 } }
        ]
        result = Article.objects.aggregate(*pipeline)
        serializer = ArticlePipelineSerializer(result, many=True)
        return Response(data={"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
