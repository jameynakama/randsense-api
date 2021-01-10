from xml.dom import minidom
import xml.etree.ElementTree as xml
from xml.etree import ElementTree as ET

from django.core.management.base import BaseCommand


# categories: {'adv', 'conj', 'pron', 'aux', 'adj', 'verb', 'noun', 'det', 'modal', 'prep'}
CATEGORIES_TO_ALWAYS_SAVE = [
    "conj",
    "pron",
    "aux",
    "det",
    "modal",
    "prep"
]


class Command(BaseCommand):
    help = "Reduce an xml file by saving every nth element"

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)
        parser.add_argument("--save-every", type=int, default=1)
        parser.add_argument("--output-file", type=str, default="reduced.xml")

    def handle(self, *args, **options):
        with open(options["filename"], "r") as infile:
            with open(options["output_file"], "w") as outfile:
                outfile.writelines([
                    '<?xml version="1.0" encoding="UTF-8"?>\n',
                    '<lexRecords>\n'
                ])
                tree = xml.parse(infile)
                root = tree.getroot()

                i = 0
                total = 0
                wrote = 0
                for element in root:
                    total += 1
                    # import ipdb; ipdb.set_trace(context=20)
                    if element.find("cat").text in CATEGORIES_TO_ALWAYS_SAVE:
                        # Write it if its in a category to always save
                        print(f"Saved at {i} because {element.find('cat').text}")
                        outfile.write(ET.tostring(element).decode())
                        wrote += 1
                        # And don't increment the index
                        continue
                    else:
                        # Save every nth item no matter what
                        i += 1
                        if i % options["save_every"] == 0:
                            print(f"Saved at {i} - {element.find('cat').text}")
                            outfile.write(ET.tostring(element).decode())
                            wrote += 1

                    if i == options["save_every"]:
                        i = 0

                outfile.write("</lexRecords>\n")

        print(f"Wrote {wrote} records from {total} total")
