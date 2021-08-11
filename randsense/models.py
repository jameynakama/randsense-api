import json
import random

from django.core import serializers
from django.contrib.postgres import fields
from django.db import models
from django.utils.functional import cached_property

from randsense.util import inflections, query_builder, parsing


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
        "det": Determiner,
        "modal": Modal,
        "special": SpecialWord,
    }
    if ":" in category:
        category = category[: category.index(":")]
    return class_map.get(category, GenericWord)


class Singleton(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ApiSettings(Singleton):
    class Meta:
        verbose_name_plural = "API Settings"

    base_word_frequency = models.BigIntegerField(default=1000000)
    grammar_source = models.TextField(null=True, blank=True)
    grammar = models.JSONField(null=True, blank=True, default=dict)

    def save(self, *args, **kwargs):
        self.grammar = parsing.parse_grammar(self.grammar_source)
        super().save(*args, **kwargs)


class Sentence(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    base = models.JSONField(default=list, blank=True)
    diagram = fields.ArrayField(models.CharField(max_length=255), null=True, blank=True)
    inflected = models.TextField(null=True, blank=True)

    incorrect_votes = models.IntegerField(default=0)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.base[:50]}"

    @cached_property
    def words(self):
        return " ".join(word["fields"]["base"] for word in self.base)

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
        self.diagram = parsing.get_sentence_diagram(ApiSettings.load().grammar)

    def fill_in_base_words(self):
        for category in self.diagram:
            new_word = self.get_random_word(category=category)
            serialized_word = serializers.serialize("json", [new_word])
            word_json = json.loads(serialized_word)[0]["fields"]
            self.base.append(word_json)

    def inflect(self):
        inflected_words = inflections.inflect(self)
        ending_punctuation = "?" if inflected_words[0] in ["what", "which"] else "."
        self.inflected = (" ".join(inflected_words)).capitalize()
        self.inflected += ending_punctuation
        self.save()

    @classmethod
    def get_random_word(cls, category):
        category, specific_type, specific_word = query_builder.get_category_and_type(category)
        klass = get_word_class(category)
        base_word_frequency = ApiSettings.load().base_word_frequency
        query = query_builder.get_query_for_category(
            klass, specific_type=specific_type, specific_word=specific_word
        ).filter(active=True)

        if specific_word:
            return query.first()
        else:
            query = query.filter(rank__gt=base_word_frequency)

            earliest_pk = int(query.earliest("pk").pk)
            latest_pk = int(query.latest("pk").pk)

            choice = None

            while choice is None:
                pk = random.randint(earliest_pk, latest_pk)
                try:
                    choice = query.get(pk=pk)
                except klass.DoesNotExist:
                    pass

            return choice


class Word(models.Model):
    class Meta:
        # TODO figure out if there's a way to do unique
        # unique_together = ["base", "category"]
        ordering = ["base"]
        abstract = True

    def __str__(self):
        return f"<{self.base} - {self.category}>"

    base = models.CharField(max_length=255)
    category = models.CharField(max_length=255, db_index=True)

    inflections = models.JSONField(default=dict, blank=True)
    attributes = models.JSONField(default=dict, blank=True)

    rank = models.BigIntegerField(default=0)

    active = models.BooleanField(default=True)


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


class Determiner(Word):
    pass


class Modal(Word):
    pass
