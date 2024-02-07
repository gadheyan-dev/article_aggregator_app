from rest_framework_mongoengine import serializers, fields
from articles.models.domain import Domain
from articles.utils.common_utils import convert_urls_to_domain

class DomainSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Domain
        read_only_fields = ['_id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Extract domain from the URL provided in the data
        url = validated_data.get('url')
        if url:
            validated_data['url'] = convert_urls_to_domain(url, many=False)
        
        return super().create(validated_data)
    
class DomainUpdateSerialier(DomainSerializer):
    class Meta(DomainSerializer.Meta):
        read_only_fields = ['_id', 'url', 'created_at', 'updated_at']


class CrawledDomainSerializer(serializers.DocumentSerializer):
    
    class Meta:
        model = Domain
        fields = ['url', 'is_crawlable']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        visited = True
        representation['visited'] = visited
        return representation