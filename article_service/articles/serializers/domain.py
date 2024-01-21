from rest_framework import serializers
from articles.models.domain import Domain

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = [ 'url', 'last_crawled_at', 'is_crawlable', 'crawl_delay_in_minutes', 'created_at', 'updated_at']
