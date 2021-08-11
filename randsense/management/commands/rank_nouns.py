import time
import mmap
import logging

import progressbar

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
    models.Modal,
]


class Command(BaseCommand):
    help = "Applies frequency rankings to words"

    def add_arguments(self, parser):
        parser.add_argument("rankings_file", type=str)
        parser.add_argument("--how-many", type=int, default=1000000)

    def handle(self, *args, **options):
        how_many = options["how_many"]
        i = 0
        queryset = models.Noun.objects.filter(rank=-1)[:how_many]
        total = queryset.count()
        widgets = ["Ranking: ", progressbar.Bar("=", "[", "]"), " ",
                   progressbar.Percentage()]
        pbar = progressbar.ProgressBar(maxval=total, widgets=widgets).start()
        with open(options["rankings_file"], newline="") as f:
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            # TODO set all to -1 and filter on that
            # so you can run it in chunks and
            # do unranked nouns each time
            for noun in queryset.iterator():
                # if (i / total).is_integer():
                #     print(f"{(i / total) * 100}%")
                # if i % 50 == 0:
                #     # print(f"\n-----\n{i}\n-----\n")
                #     print(f"{(i / total) * 100}%")
                i += 1
                pbar.update(i)
                to_find = [word for word in noun.base.split(' ') if not word.isnumeric()]
                if not len(to_find):
                    # print(f"{i}: SKIPPING {noun.base}")
                    continue
                # print(f"{i}: Looking for {noun.base}")
                for word in to_find:
                    # TODO ALL words must be in the freq file
                    # TODO manually add things like 1, 1st, etc
                    inner_word_rankings = []
                    s.seek(0)
                    position = s.find(bytes(word.lower() + ',', "utf-8"))
                    # print(f"   Looking for {word}: {position}")
                    if position != -1:
                        s.seek(position)
                        rank = s.readline().decode("utf-8").split(",")[-1]
                        inner_word_rankings.append(rank)
                        # print(f'   Found {noun.base} in file')
                        # print(f'   {s.readline()}')
                    else:
                        inner_word_rankings.append(0)
                noun.rank = min(inner_word_rankings)
                noun.save()
        pbar.finish()
