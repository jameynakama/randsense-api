import pytest
from django.core.management import call_command

from randsense import models


@pytest.fixture
def nouns():
    models.Noun.objects.create(
        base="insect",
        category="noun",
        rank=-1
    )
    models.Noun.objects.create(
        base="praying mantis",
        category="noun",
        rank=-1
    )
    models.Noun.objects.create(
        base="mantis praying",
        category="noun",
        rank=-1
    )


@pytest.mark.django_db
def test_ranks_simple_words(nouns):
    assert models.Noun.objects.get(base="insect").rank == -1
    call_command("rank_words_by_frequency", "randsense/tests/files/test_freq.csv", word_class="noun")
    assert models.Noun.objects.get(base="insect").rank == 30


@pytest.mark.django_db
def test_does_not_run_on_ranked_nouns(nouns):
    models.Noun.objects.filter(base="insect").update(rank=100)
    assert models.Noun.objects.get(base="insect").rank == 100
    call_command("rank_words_by_frequency", "randsense/tests/files/test_freq.csv", word_class="noun")
    assert models.Noun.objects.get(base="insect").rank == 100


@pytest.mark.django_db
def test_ranks_words_with_spaces(nouns):
    """Should rank multi-word words with the lowest-scoring word"""
    assert models.Noun.objects.get(base="mantis praying").rank == -1
    call_command("rank_words_by_frequency", "randsense/tests/files/test_freq.csv", word_class="noun")
    assert models.Noun.objects.get(base="mantis praying").rank == 10


@pytest.mark.django_db
def test_only_does_how_many(nouns):
    """Should rank multi-word words with the lowest-scoring word"""
    call_command("rank_words_by_frequency", "randsense/tests/files/test_freq.csv", how_many=2, word_class="noun")
    assert models.Noun.objects.get(base="insect").rank == 30
    assert models.Noun.objects.get(base="mantis praying").rank == 10
    assert models.Noun.objects.get(base="praying mantis").rank == -1


@pytest.mark.django_db
def test_ranks_unfound_words_as_zero():
    models.Noun.objects.create(base="AOFAS insect", rank=-1)
    call_command("rank_words_by_frequency", "randsense/tests/files/test_freq.csv", word_class="noun")
    assert models.Noun.objects.get(base="AOFAS insect").rank == 0


@pytest.mark.django_db
def test_finds_whole_words():
    models.Noun.objects.create(base="ntis", rank=-1)
    call_command("rank_words_by_frequency", "randsense/tests/files/test_freq.csv", word_class="noun")
    assert models.Noun.objects.get(base="ntis").rank == 0
