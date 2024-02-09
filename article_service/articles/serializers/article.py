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
        fields = ['_id', 'title', 'url', 'top_image', 'authors' ,'summary', 'publish_date']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['read_time_score'] = instance.get("read_time_score", 0)
        return representation
