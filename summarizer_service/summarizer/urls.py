from django.urls import path
from .views import KeywordExtractionView

urlpatterns = [
    path('extract/', KeywordExtractionView.as_view(), name='extract-keywords'),
]