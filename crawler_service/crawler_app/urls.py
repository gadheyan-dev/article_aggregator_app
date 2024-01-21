from django.urls import path
from crawler_app import views


urlpatterns = [
    path('find_feeds/', views.FindFeed.as_view()),
    path('parse_feeds/', views.ParseFeed.as_view())
]

