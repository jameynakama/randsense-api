import os

import pytest

from django.conf import settings
from django.core.management import call_command

from randsense import models
from randsense.util import query_builder


pytestmark = pytest.mark.usefixtures("setup")


@pytest.fixture()
def setup(db):
    call_command(
        "ingest_lexicon",
        os.path.join(
            settings.BASE_DIR, "randsense", "tests", "files", "test_lexicon.xml"
        ),
    )


def test_get_category_and_type():
    """Should get category and type"""
    assert query_builder.get_category_and_type("aminal:doge") == ["aminal", "doge", None]


def test_get_category_no_type():
    """Should get category and None if no type"""
    assert query_builder.get_category_and_type("birb") == ("birb", None, None)


def test_get_specific_word():
    """Should get category and specific word"""
    assert query_builder.get_category_and_type("birb*chickadee") == ["birb", None, "chickadee"]


def test_get_nothing():
    """Should not blow up if nothing is found"""
    query = query_builder.get_query_for_category(models.Pronoun, "dogs")
    assert query.count() == 0


def test_get_pronoun():
    """Should query for general pronouns"""
    query = query_builder.get_query_for_category(models.Pronoun)
    assert query.count() > 0


def test_get_noun():
    """Should query for general nouns"""
    query = query_builder.get_query_for_category(models.Noun)
    assert query.count() > 0


def test_get_specific_noun():
    """Should query for specific noun types"""
    query = query_builder.get_query_for_category(models.Noun, "variants:uncount")
    assert query.count() > 0
    query = query_builder.get_query_for_category(models.Noun, "variants:reg")
    assert query.count() > 0


def test_get_adverb():
    """Should query for general adverbs"""
    query = query_builder.get_query_for_category(models.Adverb)
    assert query.count() > 0


def test_get_specific_adverb_type():
    """Should query for specific adverb types"""
    query = query_builder.get_query_for_category(models.Adverb, "modification:sentence_modifier")
    assert query.count() > 0
    query = query_builder.get_query_for_category(models.Adverb, "modification:verb_modifier")
    assert query.count() > 0


def test_get_verb():
    """Should query for general verbs"""
    query = query_builder.get_query_for_category(models.Verb)
    assert query.count() > 0


def test_get_specific_verb_type():
    """Should query for specific verb types"""
    query = query_builder.get_query_for_category(models.Verb, "tran")
    assert query.count() > 0
    query = query_builder.get_query_for_category(models.Verb, "intran")
    assert query.count() > 0
