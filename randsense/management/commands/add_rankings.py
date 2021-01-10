import csv
import logging

from django.core.management.base import BaseCommand

from randsense import models


logger = logging.getLogger(__name__)


word_types = [
    models.SpecialWord,
    models.GenericWord,
    models.Noun,
    models.Verb,
    models.Adverb,
    models.Adjective,
    models.Conjunction,
    models.Pronoun,
    models.Auxiliary,
    models.Preposition,
    models.Determiner,
    models.Modal
]


class Command(BaseCommand):
    help = "Applies frequency rankings to words"

    def add_arguments(self, parser):
        parser.add_argument('rankings_file', type=str)

    def handle(self, *args, **options):
        i = 0
        with open(options['rankings_file'], newline='') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            for row in reader:
                word, ranking = row
                for Word in word_types:
                    words = Word.objects.filter(base=word)
                    for word_object in words:
                        word_object.rank = ranking
                        word_object.save()
                if i % 1000 == 0:
                    print(f"{i}: {word}::{word_object.__class__.__name__}::{ranking}")
                i += 1
