from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from summarizer.serializers import KeywordExtractionSerializer
from summarizer.utils import convert_rank_to_score


class KeywordExtractionView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = KeywordExtractionSerializer(data=request.data, many=True)
        if serializer.is_valid():
            result = []
            for validated_data in serializer.validated_data:
                text = validated_data.get("text")
                url = validated_data.get("url")

                # Process the text using spaCy and PyTextRank
                nlp = settings.NLP
                doc = nlp(text)
                keyword_obj = {"url": url, "keywords": [
                    {'text': phrase.text, 'rank': phrase.rank, 'count': phrase.count}
                    for phrase in doc._.phrases[:settings.MAXIMUM_NUMBER_OF_KEYWORDS]
                ]}
                keyword_obj = convert_rank_to_score(keyword_obj)
                result.append(keyword_obj)

            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
