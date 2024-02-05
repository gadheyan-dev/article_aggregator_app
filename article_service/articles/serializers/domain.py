from rest_framework_mongoengine import serializers
from articles.models.domain import Domain
from articles.utils import convert_urls_to_domain

class DomainSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Domain
        fields = '__all__'
        read_only_fields = ['_id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Extract domain from the URL provided in the data
        url = validated_data.get('url')
        if url:
            validated_data['url'] = convert_urls_to_domain(url, many=False)
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Extract domain from the URL provided in the data
        url = validated_data.get('url', instance.url)
        if url:
            validated_data['url']  = convert_urls_to_domain(url)

        return super().update(instance, validated_data)
