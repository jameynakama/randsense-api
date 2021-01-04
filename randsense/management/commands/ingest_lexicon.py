import os
import xml.etree.ElementTree as xml

from django.core.management.base import BaseCommand

from randsense import models


# categories: {'adv', 'conj', 'pron', 'aux', 'adj', 'verb', 'noun', 'det', 'modal', 'prep'}
# ALLOWED_ATTRIBUTES = {
#     # Verbs
#     "tran": "transitive",
#     "intran": "intransitive",
#     "ditran": "ditransitive",
#     "link": "linking",
#
#     # Nouns
#     "uncount": "noncount",
#     "place": "place",
#     "person": "person",
#     "demon": "demon",
#
#     # Pronouns
#     "dem": "demonstrative",
#     "obj": "objective",
#     "subj": "subjective"
#
#     # Adverbs
#     # Conjunctions - maybe not
#     # Auxiliary - maybe not
#     # Adjectives
#     # Determiners
#     # Modals
#     # Prepositions
# }


class Command(BaseCommand):
    help = "Creates word records from lexicon xml file"

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str)

    def handle(self, *args, **options):
        # TODO remove
        # i = 1
        # data = {}

        tree = xml.parse(options['xml_file'])
        root = tree.getroot()

        for lex_record in root:
            word = models.Word()
            for line in lex_record:
                if line.tag == "base":
                    word.base = line.text
                elif line.tag == "cat":
                    word.category = line.text

                    # TODO remove
                    # if word.category not in data:
                    #     data[word.category] = {}
                    # if "inflections" not in data[word.category]:
                    #     data[word.category]["inflections"] = set()
                    # if "attributes" not in data[word.category]:
                    #     data[word.category]["attributes"] = set()

                # Inflections
                elif line.tag == "inflVars":
                    # # TODO remove
                    # data[word.category]['inflections'].add(line.attrib['infl'])

                    # if "inflections" not in word.attributes:
                    #     word.data["inflections"] = {}
                    word.data["inflections"][line.attrib["infl"]] = line.text

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
                        # # TODO remove
                        # data[word.category]["attributes"].add(f"{entry.tag} - {entry.text}")

                        if entry.tag != "variant":
                            if entry.tag not in word.data["attributes"]:
                                word.data["attributes"][entry.tag] = []
                            word.data["attributes"][entry.tag].append(entry.text)

                # # Pronouns
                # elif line.tag == "pronEntry":
                #     for entry in line:
                #         # TODO remove
                #         data[word.category]["attributes"].add(f"{entry.tag} - {entry.text}")
                #
                #         if entry.tag == "type" and entry.text in ALLOWED_ATTRIBUTES:
                #             # TODO: Save the value of the tag and use it in generation
                #             word.attributes[ALLOWED_ATTRIBUTES[entry.text]] = True
                #
                # # Adverbs
                # elif line.tag == "advEntry":
                #     for entry in line:
                #         # TODO remove
                #         data[word.category]["attributes"].add(f"{entry.tag} - {entry.text}")
                #
                # # Conjunction (no entries)
                #
                # # Adjectives
                # elif line.tag == "adjEntry":
                #     for entry in line:
                #         # TODO remove
                #         data[word.category]["attributes"].add(f"{entry.tag} - {line.text}")
                #
                # # Determiners
                # elif line.tag == "detEntry":
                #     for entry in line:
                #         # TODO remove
                #         data[word.category]["attributes"].add(f"{entry.tag} - {line.text}")
                #
                # # Modals
                # elif line.tag == "modalEntry":
                #     for entry in line:
                #         # TODO remove
                #         data[word.category]["attributes"].add(f"{entry.tag} - {line.text}")

            word.save()

        #     i += 1
        #     if i % 1500 == 0:
        #         print(f"{i} - {word.base} - {word.category}")
        # print(f"{i} - {word.base}")

        # import pprint
        # pprint.pprint(data)
