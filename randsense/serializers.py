from rest_framework import serializers

from randsense import models


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sentence
        fields = "__all__"
