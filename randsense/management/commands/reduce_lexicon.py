import os
import xml.etree.ElementTree as xml

from django.core.management.base import BaseCommand

from randsense import models

# dcr manage dumpdata randsense --output all.json
# dcr manage reduce_lexicon
# dcr manage dumpdata randsense --indent 2 --output randsense/fixtures/test_fixtures.json
# rad randsense
# dcr manage loaddata all.json


class Command(BaseCommand):
    help = "Reduce all tables to 100 items or less, for testing"

    def add_arguments(self, parser):
        parser.add_argument("--keep", type=int, default=100)

    def handle(self, *args, **options):
        for klass in [
            models.Pronoun,
            models.Verb,
            models.Adverb,
            models.GenericWord,
            models.Adjective,
            models.Noun,
            models.Preposition,
            models.Auxiliary,
            models.Conjunction,
        ]:
            if klass.objects.count() > options["keep"]:
                keep = klass.objects.order_by("?")[: options["keep"]]
                klass.objects.exclude(pk__in=keep).delete()
                assert klass.objects.count() <= options["keep"]

        models.Sentence.objects.all().delete()

        # dcr manage dumpdata randsense --output randsense/fixtures/test_fixtures.yaml
