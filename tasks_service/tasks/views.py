from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tasks import summarize_and_save

class TaskList(APIView):
    
    def post(self, request, format=None):
        
        result = summarize_and_save.delay(request.data)
        return Response({'task_id': result.id})
            


