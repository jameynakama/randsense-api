from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def vote_to_remove(request, word_type=None, pk=None):
    if request.method != "POST":
        return HttpResponse(status=404)

    klass = models.CLASS_MAP.get(word_type)
    if not klass:
        return JsonResponse({
            "error": f"Word type '{word_type}' does not exist.",
            "available_types": list(models.CLASS_MAP.keys())
        }, status=400)

    word = get_object_or_404(klass, pk=pk)
    word.removal_votes += 1
    word.save()

    response = {
        "pk": word.pk,
        "base": word.base,
        "removal_votes": word.removal_votes
    }

    return JsonResponse(response)


@csrf_exempt
def mark_sentence_incorrect(request, pk=None):
    if request.method != "POST":
        return HttpResponse(status=404)

    sentence = get_object_or_404(models.Sentence, pk=pk)
    sentence.incorrect_votes += 1
    sentence.save()

    response = {
        "pk": sentence.pk,
        "base": sentence.inflected,
        "incorrect_votes": sentence.incorrect_votes
    }

    return JsonResponse(response)
