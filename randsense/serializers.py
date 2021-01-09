from rest_framework import serializers

from randsense import models


class SentenceSerializer(serializers.ModelSerializer):
    words = serializers.ReadOnlyField()

    class Meta:
        model = models.Sentence
        fields = "__all__"


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Word
        fields = "__all__"
