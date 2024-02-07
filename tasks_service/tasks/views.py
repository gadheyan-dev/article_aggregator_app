from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.tasks import save_articles, find_rss_feeds_from_url, parse_feeds

class SaveArticlesTaskList(APIView):
    
    def post(self, request, format=None):
        
        result = save_articles.delay(request.data)
        return Response({'task_id': result.id})
    

class CrawlTaskList(APIView):
    
    def post(self, request, format=None):
        result = find_rss_feeds_from_url.delay(request.data)
        return Response({'task_id': result.id})
            

class ParseFeedsList(APIView):
    
    def post(self, request, format=None):
        result = parse_feeds.delay(request.data)
        return Response({'task_id': result.id})
            
