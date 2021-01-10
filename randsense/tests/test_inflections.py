from django.test import TestCase

from randsense.util import inflections

WORDS = {
    "a": {
        "fields": {
            "base": "a",
            "category": "det",
            "attributes": {
                "sing": True
            }
        }
    },
    "all": {
        "fields": {
            "base": "all",
            "category": "det",
            "attributes": {
                "plur": True
            }
        }
    },
    "blue": {
        "fields": {
            "base": "blue",
            "category": "adj",
            "attributes": {
                "sing": True
            }
        }
    },
    "bird": {
        "fields": {
            "base": "bird",
            "category": "noun",
            "inflections": {
                "singular": "bird",
                "plural": "birds",
            }
        }
    },
    "fly": {
        "fields": {
            "base": "fly",
            "category": "verb",
            "attributes": {
                "intran": True
            },
            "inflections": {
                "pres3s": "flies"
            }
        }
    }
}


class DeterminerAndNounTestCase(TestCase):
    def test_singular_determiner(self):
        """Should use the base form of the noun"""
        diagram = ["det", "adj", "noun", "verb:intran"]
        sentence_data = [
            WORDS["a"],
            WORDS["blue"],
            WORDS["bird"],
            WORDS["fly"],
        ]
        sentence = inflections.inflect(diagram, sentence_data)
        print(sentence)
        assert " ".join(sentence) == "a blue bird fly"

    def test_plural_determiner(self):
        """Should use the plural form of the noun"""
        diagram = ["det", "noun", "verb:intran"]
        sentence_data = [
            WORDS["all"],
            WORDS["bird"],
            WORDS["fly"],
        ]
        sentence = inflections.inflect(diagram, sentence_data)
        print(sentence)
        assert " ".join(sentence) == "all birds fly"
