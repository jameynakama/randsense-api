from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings

from randsense import models, serializers


class CreateSentenceMixin:
    """Create a model instance. Stolen from DRF."""

    def create(self, request, *args, **kwargs):
        sentence = models.Sentence.create_random_sentence()
        serializer = serializers.SentenceSerializer(sentence)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class SentenceViewset(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    CreateSentenceMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Sentence.objects.all()
    serializer_class = serializers.SentenceSerializer

    def create(self, request, *args, **kwargs):
        sentence = models.Sentence.create_random_sentence()
        return Response(self.serializer_class(sentence).data)

    # For incorrect sentences
    # TODO: Turn this into a custom function
    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(id=kwargs.get('pk'))
        instance.incorrect_votes += 1
        instance.save()
        return Response(self.serializer_class(instance).data)
