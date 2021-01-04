import hashlib
import os
import random
from collections import defaultdict

from django.db import models
from django.core.cache import cache
from django.conf import settings
from django.contrib.postgres import fields

from randsense import parsing

# TODO
# Needs to be A LOT faster, rework DB structure
# Figure out queries for sub types of words (tran verb, adv mod, etc.)


class Sentence(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    base = models.TextField(null=True, blank=True)
    diagram = fields.ArrayField(models.CharField(max_length=255), null=True, blank=True)
    inflected = models.TextField(null=True, blank=True)

    is_correct = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.base[:50]}"

    @classmethod
    def create_random_sentence(cls):
        # TODO Test
        sentence = Sentence()
        sentence.get_random_diagram()
        sentence.fill_in_base_words()
        sentence.save()
        return sentence

    def get_random_diagram(self):
        # TODO Test
        self.diagram = parsing.get_sentence_diagram("S")

    def fill_in_base_words(self):
        base = []
        for pos in self.diagram:
            if "_" in pos:
                new_word = Word.objects.random(category=pos[:pos.index("_")], additional=pos[pos.index("_") + 1:])
            else:
                new_word = Word.objects.random(category=pos)
            # technical_sentence.append(new_word)
            base.append(new_word.base)
            self.base = " ".join(base)


class WordManager(models.Manager):
    def random(self, **kwargs):
        # TODO Caching or better queries
        if 'additional' in kwargs:
            kwargs[kwargs['additional']] = True
            del kwargs['additional']
        choices = Word.objects.filter(**kwargs)
        return random.choice(choices)


def default_data_json():
    return {
        "inflections": {},
        "attributes": {}
    }


class Word(models.Model):
    class Meta:
        # TODO figure out if there's a way to do unique
        # unique_together = ["base", "category"]
        ordering = ["-base"]

    objects = WordManager()

    base = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    data = models.JSONField(default=default_data_json)

    # # verbs
    # past = models.CharField(max_length=255, blank=True)
    # past_participle = models.CharField(max_length=255, blank=True)
    # present_participle = models.CharField(max_length=255, blank=True)
    # present3s = models.CharField(max_length=255, blank=True)
    # transitive = models.BooleanField(blank=True)
    # intransitive = models.BooleanField(blank=True)
    # ditransitive = models.BooleanField(blank=True)
    # linking = models.BooleanField(blank=True)
    #
    # # nouns
    # plural = models.CharField(max_length=255, blank=True)
    # noncount = models.BooleanField(blank=True)
    # place = models.BooleanField(blank=True)
    # person = models.BooleanField(blank=True)
    # demon = models.BooleanField(blank=True)
    #
    # # adjectives
    # predicative = models.BooleanField(blank=True)
    # qualitative = models.BooleanField(blank=True)
    # classifying = models.BooleanField(blank=True)
    # comparative = models.BooleanField(blank=True)
    # superlative = models.BooleanField(blank=True)
    # color = models.BooleanField(blank=True)
    #
    # # adverbs
    # sentence_modifier = models.BooleanField(blank=True)
    # verb_modifier = models.BooleanField(blank=True)
    # intensifier = models.BooleanField(blank=True)
    #
    # # determiners
    # is_plural = models.BooleanField(blank=True)
    # coordinating = models.BooleanField(blank=True)
    #
    # # other
    # and_literal = models.BooleanField(blank=True)

    def __str__(self):
        return f"<{self.base} - {self.category}>"
