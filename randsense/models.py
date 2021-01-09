import json
import random

from django.core import serializers
from django.contrib.postgres import fields
from django.db import models
from django.utils.functional import cached_property

from randsense import parsing


# categories: {'adv', 'conj', 'pron', 'aux', 'adj', 'verb', 'noun', 'det', 'modal', 'prep'}
def get_word_class(category):
    class_map = {
        "noun": Noun,
        "verb": Verb,
        "adj": Adjective,
        "adv": Adverb,
        "conj": Conjunction,
        "pron": Pronoun,
        "aux": Auxiliary,
        "prep": Preposition,
        "special": SpecialWord
    }
    if ":" in category:
        category = category[:category.index(":")]
    return class_map.get(category, GenericWord)


class Sentence(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    base = models.JSONField(default=list, blank=True)
    diagram = fields.ArrayField(models.CharField(max_length=255), null=True, blank=True)
    inflected = models.TextField(null=True, blank=True)

    is_correct = models.BooleanField(default=True)

    @cached_property
    def words(self):
        return " ".join(word["fields"]["base"] for word in self.base)

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
        sentence.inflect()
        sentence.save()
        return sentence

    def get_random_diagram(self):
        # TODO Test
        self.diagram = parsing.get_sentence_diagram()

    def fill_in_base_words(self):
        for category in self.diagram:
            new_word = self.get_random_word(category=category)
            serialized_word = serializers.serialize("json", [new_word])
            word_json = json.loads(serialized_word)[0]
            self.base.append(word_json)

    def inflect(self):
        pass

    @classmethod
    def get_random_word(cls, category):
        # TODO Caching or better queries
        klass = get_word_class(category)

        if ":" in category:
            base_type, specific_type = category.split(":", 1)
            choices = klass.objects.filter(category=base_type, **{f"attributes__{specific_type}__isnull": False})
        else:
            choices = klass.objects.filter(category=category)

        earliest_pk = int(choices.earliest("pk").pk)
        latest_pk = int(choices.latest("pk").pk)

        choice = None

        while choice is None:
            pk = random.randint(earliest_pk, latest_pk)
            try:
                choice = choices.get(pk=pk)
            except klass.DoesNotExist:
                pass

        return choice


class Word(models.Model):
    class Meta:
        # TODO figure out if there's a way to do unique
        # unique_together = ["base", "category"]
        ordering = ["-base"]
        abstract = True

    def __str__(self):
        return f"<{self.base} - {self.category}>"

    base = models.CharField(max_length=255)
    category = models.CharField(max_length=255, db_index=True)

    inflections = models.JSONField(default=dict, blank=True)
    attributes = models.JSONField(default=dict, blank=True)


class SpecialWord(Word):
    pass


class GenericWord(Word):
    pass


class Noun(Word):
    pass


class Verb(Word):
    pass


class Adverb(Word):
    pass


class Adjective(Word):
    pass


class Conjunction(Word):
    pass


class Pronoun(Word):
    pass


class Auxiliary(Word):
    pass


class Preposition(Word):
    pass
