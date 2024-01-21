from django.urls import path
from .views import article, domain

urlpatterns = [
    path("articles/", article.ArticleAPI.as_view()),
    path("domains/", domain.DomainAPI.as_view()),
    path("domains/check_crawled", domain.CheckCrawledDomainAPI.as_view())
]