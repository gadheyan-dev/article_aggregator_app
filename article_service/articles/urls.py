from django.urls import path
from .views import article, domain

urlpatterns = [
    path("articles/", article.ArticleListAPI.as_view()),
    path("domains/", domain.DomainsAPI.as_view()),
    path("domains/check_crawled", domain.CheckCrawledDomainAPI.as_view())
]