from rest_framework import serializers

class KeywordExtractionSerializer(serializers.Serializer):
    url = serializers.URLField()
    text = serializers.CharField()