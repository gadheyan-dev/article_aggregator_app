from rest_framework_mongoengine import serializers, fields
from articles.models.article import Article
from mongoengine import ValidationError 


class ArticleSerializer(serializers.DocumentSerializer):

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['_id', 'created_at', 'updated_at']


class ArticlePipelineSerializer(serializers.DocumentSerializer):

    class Meta:
        model = Article
        fields = ['_id', 'title', 'url', 'top_image', 'read_time_in_minutes', 'authors' ,'summary', 'publish_date']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['title_score'] = instance.get("title_score", 0)
        # representation['category_score'] = instance.get("category_score", 0)
        # representation['read_time_score'] = instance.get("read_time_score", 0)
        # representation['recency_score'] = instance.get("recency_score", 0)
        # representation['keyword_score'] = instance.get("keyword_score", 0)
        # representation['inbound_domain_score'] = instance.get("inbound_domain_score", 0)
        representation['domain'] = instance.get("domain", 0)
        representation['total_score'] = instance.get("total_score", 0)
        return representation
