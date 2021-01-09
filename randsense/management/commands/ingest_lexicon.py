import os
import xml.etree.ElementTree as xml

from django.core.management.base import BaseCommand

from randsense import models


# categories: {'adv', 'conj', 'pron', 'aux', 'adj', 'verb', 'noun', 'det', 'modal', 'prep'}

"""
noun
['compl', 'nominalization', 'proper', 'tradeName', 'trademark', 'variants']

adj
['compl', 'nominalization', 'position', 'stative', 'variants']

verb
['cplxtran', 'ditran', 'intran', 'link', 'nominalization', 'tran', 'variants']

adv
['interrogative', 'modification', 'negative', 'variants']

pron
['gender', 'interrogative', 'type', 'variants']

det
['demonstrative', 'interrogative', 'variants']

aux
['variant']

modal
['variant']

prep
conj
compl
"""


class Command(BaseCommand):
    help = "Creates word records from lexicon xml file"

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str)

    def handle(self, *args, **options):
        # TODO remove
        i = 1
        data = {}

        tree = xml.parse(options['xml_file'])
        root = tree.getroot()

        for lex_record in root:
            word = models.GenericWord()
            for line in lex_record:
                if line.tag == "base":
                    word.base = line.text
                elif line.tag == "cat":
                    word.category = line.text

                    # TODO remove
                    if word.category not in data:
                        data[word.category] = {}
                    if "inflections" not in data[word.category]:
                        data[word.category]["inflections"] = set()
                    if "attributes" not in data[word.category]:
                        data[word.category]["attributes"] = set()
                        data[word.category]["tags"] = set()

                # Inflections
                elif line.tag == "inflVars":
                    # TODO remove
                    data[word.category]['inflections'].add(line.attrib['infl'])

                    word.inflections[line.attrib["infl"]] = line.text

                # # Verbs
                # elif line.tag == "verbEntry":
                #     for entry in line:
                #         # TODO remove
                #         data[word.category]["attributes"].add(entry.tag)
                #
                #         if entry.tag != "variant":
                #             if entry.tag not in word.attributes:
                #                 word.attributes[entry.tag] = []
                #             # TODO: Save the value of the tag and use it in generation
                #             word.attributes[entry.tag] = entry.text

                elif line.tag == f"{word.category}Entry":
                    for entry in line:
                        # TODO remove
                        data[word.category]["attributes"].add(f"{entry.tag} - {entry.text}")
                        data[word.category]["tags"].add(entry.tag)

                        # `variant` seems to be repeats of inflections
                        if entry.tag != "variant":
                            if entry.tag == "type":
                                # `type` specifically marks types of words
                                # so save it as True for querying
                                word.attributes[entry.text] = True
                            else:
                                # Otherwise, save the text under the tag
                                if entry.tag not in word.attributes:
                                    word.attributes[entry.tag] = []
                                word.attributes[entry.tag].append(entry.text)

            cls = models.get_word_class(word.category)
            word.__class__ = cls
            word.save()

            i += 1
            if i % 10000 == 0:
                print(f"{i} - {word.base} - {word.category}")
        print(f"{i} - {word.base}")

        import pprint
        for key in data:
            data[key]['attributes'] = sorted(data[key]['attributes'])
            data[key]["tags"] = sorted(data[key]["tags"])
            data[key]['inflections'] = sorted(data[key]['inflections'])
        pprint.pprint(data)
        for key in data:
            print(key)
            pprint.pprint(data[key]["tags"])
