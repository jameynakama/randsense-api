"""
- Make favorite button tell browser to load a sentence after reload
- Add proper nouns
- Weighted paths

- Make 'ye' work more complexly
- Add negations
- Add commas
- Add some new tenses
- Adjectives: comparative, superlative
- Make "Warriors engage" possible (right now the logic is in place only for "a warrior" or "the warriors")
- Determiners can have <singularorplural/> tag, so check for this and do a choice on the noun if so
"""

import os
import random

from django.conf import settings


def parse_grammar_file():
    """Parse the grammar file into a dictionary"""
    # TODO
    # possible_types = (
    #     'indicative',
    #     )
    # self.base_sentence_type = random.choice(possible_types)

    data = open(os.path.join(os.path.dirname(__file__), 'grammar.txt'), 'r').read().split('\n')

    processed_data = []

    for line in data:
        # delete comments and blank lines from grammar data
        if not line or line[0] == '#':
            continue
        processed_data.append(line.split(' -> '))

    grammar = {}
    for element in processed_data:
        if element[0] not in grammar:
            grammar[element[0]] = []
        for item in element[1].split(' | '):
            grammar[element[0]].append(item.split(' '))

    # import pprint
    # pprint.pprint(grammar)
    return grammar


def get_sentence_diagram(starting_point="S"):
    """Create a random sentence diagram"""
    def go(level):
        if level in settings.SENTENCE_GRAMMAR:
            weights = []
            choices = settings.SENTENCE_GRAMMAR[level]
            for choice in choices:
                try:
                    float(choice[-1])
                    weights.append(float(choice[-1]))
                except ValueError:
                    choice.append("1.0")
                    weights.append(1.0)
            next_choices = []
            for i in range(len(choices)-1, -1, -1):
                if weights[i] > random.random():
                    next_choices.append(choices[i][:-1])
            next_choice = random.choice(next_choices)
            for element in next_choice:
                go(element)
        else:
            if level != '_':
                result.append(level)
                print(result)

    result = []
    go(starting_point)
    return result
