import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from randsense import models


class RandomWordManagerTestCase(TestCase):
    fixtures = ["test_fixtures.json"]

    def test_can_query_for_nouns(self):
        """Should be able to query for random nouns"""
        word = models.Sentence.get_random_word(category="noun")
        assert word.category == "noun"

    # def test_can_query_for_noun_types(self):
    #     """Should be able to query for random verb types"""
    #     noun_types = [
    #         "compl",
    #         "proper",
    #         "reg",
    #     ]
    #     for type in noun_types:
    #         word = models.Sentence.get_random_word(f"noun:{type}")
    #         assert word.category == "noun"
    #         assert type in word.attributes

    def test_can_query_for_verbs(self):
        """Should be able to query for random verbs"""
        word = models.Sentence.get_random_word(category="verb")
        assert word.category == "verb"

    def test_can_query_for_verb_types(self):
        """Should be able to query for random verb types"""
        verb_types = ["intran", "tran", "ditran", "link"]
        for category in verb_types:
            word = models.Sentence.get_random_word(f"verb:{category}")
            assert word.category == "verb"
            assert category in word.attributes

    def test_can_query_for_pronouns(self):
        """Should be able to query for random pronouns"""
        word = models.Sentence.get_random_word(category="pron")
        assert word.category == "pron"

    def test_can_query_for_pronoun_types(self):
        """Should be able to query for random pronoun types"""
        pronoun_types = [
            "dem",
            "obj",
            "subj",
            "poss",
        ]
        for category in pronoun_types:
            word = models.Sentence.get_random_word(f"pron:{category}")
            assert word.category == "pron"
            assert category in word.attributes
