from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.tasks import summarize_and_save

class SummarizeTaskList(APIView):
    
    def post(self, request, format=None):
        
        result = summarize_and_save.delay(request.data)
        return Response({'task_id': result.id})
    

# class CrawlTaskList(APIView):
    
#     def post(self, request, format=None):
#         result = find_rss_feeds_from_url.delay(request.data)
#         return Response({'task_id': result.id})
            


