from rest_framework_mongoengine import serializers
from articles.models.article import Article

        
class ArticleSerializer(serializers.DocumentSerializer):
    
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['_id', 'created_at', 'updated_at']