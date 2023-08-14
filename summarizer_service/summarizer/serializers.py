from rest_framework import serializers
from .models import Author, Article

class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    avatar = serializers.URLField(max_length=2000, allow_blank=True)
    email = serializers.EmailField(allow_blank=True)

class ArticleSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=1000)
    url = serializers.URLField(max_length=2000)
    top_image = serializers.URLField(max_length=2000)
    description = serializers.CharField(max_length = 2000, allow_blank=True)
    summary = serializers.CharField(allow_blank=True)
    publish_date = serializers.DateTimeField(input_formats=['%d-%m-%Y',])
    authors = serializers.ListField(child=AuthorSerializer())