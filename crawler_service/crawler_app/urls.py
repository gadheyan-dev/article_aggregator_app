from django.urls import path
from crawler_app import views


urlpatterns = [
    path('find_feeds/', views.FindFeed.as_view())
]

