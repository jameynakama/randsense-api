import os

import pytest

from django.conf import settings
from django.core.management import call_command

from randsense import models, query_schema


pytestmark = pytest.mark.usefixtures("setup")


@pytest.fixture()
def setup(db):
    # TODO What the f, get this to work on a module level. It's slow as hell.
    call_command(
        "ingest_lexicon",
        os.path.join(settings.BASE_DIR, "randsense", "tests", "files",
                     "test_lexicon.xml")
    )


def test_get_category_and_type():
    """Should get category and type"""
    assert query_schema.get_category_and_type("aminal:doge") == ["aminal", "doge"]


def test_get_category_no_type():
    """Should get category and None if no type"""
    assert query_schema.get_category_and_type("birb") == ("birb", None)


def test_get_nothing():
    """Should not blow up if nothing is found"""
    query = query_schema.get_query_for_category(models.Pronoun, "dogs")
    assert query.count() == 0


def test_get_pronoun():
    """Should query for general pronouns"""
    query = query_schema.get_query_for_category(models.Pronoun)
    assert query.count() > 0


def test_get_specific_pronoun():
    """Should query for specific pronouns"""
    query = query_schema.get_query_for_category(models.Pronoun, "obj")
    assert query.count() > 0


def test_get_noun():
    """Should query for general nouns"""
    query = query_schema.get_query_for_category(models.Noun)
    assert query.count() > 0


def test_get_specific_noun():
    """Should query for specific nouns"""
    query = query_schema.get_query_for_category(models.Noun, "uncount")
    assert query.count() > 0
    query = query_schema.get_query_for_category(models.Noun, "reg")
    assert query.count() > 0


def test_get_adverb():
    """Should query for general adverbs"""
    query = query_schema.get_query_for_category(models.Adverb)
    assert query.count() > 0


def test_get_specific_adverb():
    """Should query for specific adverbs"""
    query = query_schema.get_query_for_category(models.Adverb, "sentence_modifier")
    assert query.count() > 0
    query = query_schema.get_query_for_category(models.Adverb, "verb_modifier")
    assert query.count() > 0


def test_get_verb():
    """Should query for general verbs"""
    query = query_schema.get_query_for_category(models.Verb)
    assert query.count() > 0


def test_get_specific_verb():
    """Should query for specific verbs"""
    query = query_schema.get_query_for_category(models.Verb, "tran")
    assert query.count() > 0
    query = query_schema.get_query_for_category(models.Verb, "intran")
    assert query.count() > 0
