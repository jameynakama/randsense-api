import logging
import random


log = logging.getLogger(__name__)

VOWELS = ["a", "e", "i", "o", "u"]

BE = {
    "present": {
        "i": "am",
        "you": "are",
        "it": "is",
        "plural": "are",
    },
    "simple_past": {
        "i": "was",
        "you": "were",
        "it": "was",
        "plural": "were",
    },
}

verb_types = [
    "verb-intransitive",
    "verb-transitive",
    "verb-ditransitive",
]


def inflect(sentence):
    # 1. inflect nouns by examining their determiners
    sentence = inflect_nouns(sentence)

    # 2. conjugate verbs by finding their subjects (and determiners)
    sentence = inflect_verbs(sentence)

    # 3. make indefinite articles agree
    sentence = make_articles_agree(sentence)

    # 4. add any special punctuation
    sentence = add_punctuation(sentence)

    inflected_sentence = [word.get("inflected", word["base"])
                          for word in sentence.base]

    return inflected_sentence


def inflect_nouns(sentence):
    diagram_to_process = sentence.diagram.copy()
    diagram_to_process = [pos.split("*")[0] for pos in diagram_to_process]
    while "det" in diagram_to_process:
        # find all determiners and their following nouns for pluralization
        determiner_index = diagram_to_process.index("det")

        if any(
            [
                variant in ["plur", "free", "singuncount", "pluruncount"]
                for variant in sentence.base[determiner_index]["attributes"][
                    "variants"
                ]
            ]
        ):
            noun_index = -1
            for i in range(determiner_index + 1, len(diagram_to_process)):
                if diagram_to_process[i].startswith("noun"):
                    noun_index = i
                    break
            if noun_index >= 0:
                sentence.base[noun_index]["inflected"] = pluralize_noun(sentence.base[noun_index])
                diagram_to_process[noun_index] = "noun-inflected"
        diagram_to_process[determiner_index] = "determiner-done"

    return sentence


def inflect_verbs(sentence):
    diagram = ["verb" if pos.startswith("verb") else pos for pos in sentence.diagram]
    while "verb" in diagram:
        # Find all verbs and their preceding subjects and determiners
        verb_index = [
            diagram.index(pos)
            for pos in diagram
            if pos == "verb"
        ][0]
        determiner_index = -1
        subject_index = -1
        for i in range(verb_index, -1, -1):
            if diagram[i] in ["det"]:
                determiner_index = i
                break
        for i in range(verb_index, -1, -1):
            if diagram[i] in ["noun"]:
                subject_index = i
                break

        sentence.base[verb_index]["inflected"] = do_verb(
            sentence.base[subject_index],
            sentence.base[verb_index],
            any(
                [
                    variant in ["plur", "free", "singuncount", "pluruncount"]
                    for variant in sentence.base[determiner_index][
                        "attributes"
                    ]["variants"]
                ]
            ),
        )

        diagram[verb_index] = "verb-conjugated"

    return sentence


def make_articles_agree(sentence):
    """Fix things like "an uniform", "an unicycle", etc."""
    for i, word in enumerate(sentence.base):
        if word["base"] in ["a", "an"]:
            next_word = sentence.base[i + 1]
            if next_word["base"][0] in ["a", "e", "i", "o", "u"]:
                if not next_word["base"].startswith("uni"):
                    sentence.base[i]["inflected"] = "an"
                else:
                    sentence.base[i]["inflected"] = "a"
            else:
                sentence.base[i]["inflected"] = "a"
    return sentence


def add_punctuation(sentence):
    for i, word in enumerate(sentence.base):
        if word["category"] == "punc":
            sentence.base[i]["inflected"] = word["attributes"]["base"]
    return sentence


def pluralize_noun(noun):
    # take into account uncount and pluruncount
    if "plural" in noun["inflections"]:
        noun = noun["inflections"]["plural"]
    else:
        noun = noun["inflections"]["singular"]
        if noun[-2:] in [
            "ey",
            "ay",
        ]:
            noun = noun + "s"
        elif noun[-1] in [
            "y",
        ]:
            noun = noun[:-1] + "ies"
        elif noun[-2:] in [
            "ss",
            "ch",
        ]:
            noun = noun + "es"
        elif noun[-1] in [
            "s",
        ]:
            noun = noun + "ses"
        else:
            noun = noun + "s"
    return noun


def do_verb(subject, verb, is_plural):
    tense = random.choice(
        [
            "present",
            "past",
        ]
    )

    if verb["base"] == "be":
        return conjugate_for_be(subject, tense, is_plural)

    if tense == "present":
        return conjugate_for_present(subject, verb, is_plural)
    elif tense == "past":
        return conjugate_for_simple_past(verb)


def conjugate_for_present(subject, verb, is_plural):
    if is_plural:
        return verb["inflections"]["base"]
    else:
        if subject["base"] not in [
            "i",
            "you",
            "we",
            "they",
        ]:
            if verb["inflections"]["pres3s"]:
                return verb["inflections"]["pres3s"]
            else:
                if verb["base"][-1] == "y" and verb.base[-2:] != "ey":
                    return verb["base"][:-1] + "ies"
                elif verb["base"][-1] == "x":
                    return verb["base"] + "es"
                elif verb["base"][-2:] in ["sh", "ch", "ss"]:
                    return verb["base"] + "es"
                else:
                    return verb["base"] + "s"
        else:
            return verb["base"]


def conjugate_for_simple_past(verb):
    if verb["inflections"].get("past"):
        return verb["inflections"]["past"]
    else:
        if verb["base"][-1] == "e":
            return verb.base + "d"
        elif verb["base"][-2:] in [
            "ey",
            "ay",
        ]:
            return verb["base"] + "ed"
        elif verb["base"][-1] == "y":
            return verb["base"][:-1] + "ied"
        else:
            return verb["base"] + "ed"


def conjugate_for_be(subject, tense, is_plural):
    if is_plural:
        new_verb = BE[tense]["plural"]
    else:
        if subject.base not in [
            "i",
            "you",
        ]:
            new_verb = BE[tense]["it"]
        else:
            new_verb = BE[tense][subject.base]

    return new_verb
