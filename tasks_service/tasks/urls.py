from django.urls import path
from . import views

urlpatterns = [
    path("save_articles/", views.SaveArticlesTaskList.as_view()),
    path("crawl/", views.CrawlTaskList.as_view()),
]