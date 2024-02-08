from django.urls import path
from .views import article, domain

urlpatterns = [
    path("articles/", article.ArticleListAPI.as_view(), name='article-list'),
    path("domains/", domain.DomainsAPI.as_view(), name='domain-list'),
    path("domains/check_crawled", domain.CheckCrawledDomainAPI.as_view(), name='check-crawled-domain')
]