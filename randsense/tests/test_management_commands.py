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
        word = models.Word.objects.get(base="jump", category="verb")
        assert word.base == "jump"
        assert word.category == "verb"

    def test_saves_inflections_for_verbs(self):
        """Should save the inflections for verbs"""
        word = models.Word.objects.get(data__inflections__pastPart="gone")
        assert word.base == "go"
        assert word.category == "verb"
        assert word.data["inflections"]["past"] == "went"
        assert word.data["inflections"]["pres3s"] == "goes"
        assert word.data["inflections"]["pastPart"] == "gone"
        assert word.data["inflections"]["presPart"] == "going"

    def test_saves_verb_types(self):
        """Should save the type of verb"""
        word = models.Word.objects.get(data__inflections__pastPart="gone")
        assert word.base == "go"
        assert word.category == "verb"
        assert "intran;part(without)" in word.data["attributes"]["intran"]
        assert "intran;part(on)" in word.data["attributes"]["intran"]
        assert "np" in word.data["attributes"]["tran"]
        assert "pphr(about,np)" in word.data["attributes"]["tran"]
        assert "adj" in word.data["attributes"]["link"]
        assert "advbl" in word.data["attributes"]["link"]
        assert "ditransitive" not in word.data["attributes"]

    def test_saves_demonstrative_pronouns(self):
        """Should save demonstrative pronouns"""
        word = models.Word.objects.get(base="this", category="pron")
        assert word.base == "this"
        assert word.category == "pron"
        assert "dem" in word.data["attributes"]["type"]
        assert "obj" in word.data["attributes"]["type"]
        assert "subj" in word.data["attributes"]["type"]
