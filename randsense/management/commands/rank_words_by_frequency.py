import mmap
import logging

import progressbar

from django.core.management.base import BaseCommand

from randsense import models


logger = logging.getLogger(__name__)


word_types = {
    "adjective": models.Adjective,
    "adverb": models.Adverb,
    "conjunction": models.Conjunction,
    "determiner": models.Determiner,
    "noun": models.Noun,
    "preposition": models.Preposition,
    "pronoun": models.Pronoun,
    "verb": models.Verb
}


class Command(BaseCommand):
    help = "Applies frequency rankings to words"

    def add_arguments(self, parser):
        parser.add_argument("rankings_file", type=str)
        parser.add_argument("--word-class", "-c", type=str, required=True)
        parser.add_argument("--how-many", "-n", type=int, default=0)
        parser.add_argument("--write-misses", "-w", action="store_true", default=False)

    def handle(self, *args, **options):
        how_many = options["how_many"]

        try:
            WordClass = word_types[options["word_class"]]
        except KeyError:
            print(f"Provide one of the following classes for --word-class: {list(word_types.keys())}")
            exit(1)
            return

        queryset = WordClass.objects.filter(rank=-1)
        if how_many > 0:
            queryset = queryset[:how_many]

        total = queryset.count()

        widgets = ["Ranking: ", progressbar.Bar("=", "[", "]"), " ",
                   progressbar.Percentage()]
        pbar = progressbar.ProgressBar(maxval=total, widgets=widgets).start()

        i = 0
        ranked = 0
        unranked = []
        with open(options["rankings_file"], newline="") as f:
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            for word_object in queryset.iterator():
                i += 1
                pbar.update(i)
                to_find = [word for word in word_object.base.split(' ') if not word.isnumeric()]
                if not len(to_find):
                    continue
                inner_word_rankings = []
                for word in to_find:
                    s.seek(0)
                    position = s.rfind(bytes('\n' + word.lower() + ',', "utf-8"))
                    if position != -1:
                        s.seek(position)
                        s.readline()  # Read a line; \n leaves us on the previous one
                        rank = s.readline().decode("utf-8").split(",")[-1]
                        inner_word_rankings.append(int(rank))
                    else:
                        inner_word_rankings.append(0)
                word_object.rank = min(inner_word_rankings)
                word_object.save()
                if word_object.rank > 0:
                    ranked += 1
                else:
                    unranked.append(word_object.base)
        pbar.finish()
        print(f"Total processed: {total}")
        print(f"Ranked: {ranked}")
        print(f"Unranked: {len(unranked)}")
        if options["write_misses"]:
            with open("unranked.txt", "w") as f:
                for word in unranked:
                    f.write(word + '\n')
