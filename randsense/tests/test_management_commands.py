import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from randsense import models


class IngestLexiconTestCase(TestCase):
    def setUp(self) -> None:
        call_command(
            "ingest_lexicon",
            os.path.join(settings.BASE_DIR, "randsense", "tests", "files",
                         "test_lexicon.xml")
        )

    def test_creates_records_with_correct_base_and_category(self):
        """Should create words with the correct base form and category"""
        word = models.Verb.objects.get(base="jump")
        assert word.base == "jump"
        assert word.category == "verb"

    def test_saves_inflections_for_verbs(self):
        """Should save the inflections for verbs"""
        word = models.Verb.objects.get(inflections__pastPart="gone")
        assert word.base == "go"
        assert word.category == "verb"
        assert word.inflections["past"] == "went"
        assert word.inflections["pres3s"] == "goes"
        assert word.inflections["pastPart"] == "gone"
        assert word.inflections["presPart"] == "going"

    def test_saves_verb_types(self):
        """Should save the type of verb"""
        word = models.Verb.objects.get(inflections__pastPart="gone")
        assert word.base == "go"
        assert word.category == "verb"
        assert "intran;part(without)" in word.attributes["intran"]
        assert "intran;part(on)" in word.attributes["intran"]
        assert "np" in word.attributes["tran"]
        assert "pphr(about,np)" in word.attributes["tran"]
        assert "adj" in word.attributes["link"]
        assert "advbl" in word.attributes["link"]
        assert "ditransitive" not in word.attributes

    def test_saves_demonstrative_pronouns(self):
        """Should save demonstrative pronouns"""
        word = models.Pronoun.objects.get(base="this")
        assert word.base == "this"
        assert word.category == "pron"
        assert "dem" in word.attributes
        assert "obj" in word.attributes
        assert "subj" in word.attributes

    def test_saves_determiners(self):
        """Should save determiners"""
        both = models.GenericWord.objects.get(base="both")
        enough = models.GenericWord.objects.get(base="enough")
        every = models.GenericWord.objects.get(base="every")
        assert "plur" in both.attributes
        assert "pluruncount" in enough.attributes
        assert "sing" in every.attributes
