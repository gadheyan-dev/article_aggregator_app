from django.urls import path
from . import views

urlpatterns = [
    path("summarize/", views.SummarizeTaskList.as_view()),
    path("crawl/", views.CrawlTaskList.as_view())
]