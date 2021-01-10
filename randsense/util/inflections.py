import random


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

verb_types = ["verb-intransitive", "verb-transitive", "verb-ditransitive",]


def inflect(diagram, sentence):
    bare_sentence = [word["fields"]["base"] for word in sentence]

    #1. inflect nouns by examining their determiners
    return route_nouns(diagram, bare_sentence, sentence)

    #2. conjugate verbs by finding their subjects (and determiners)
    # self.route_verbs(base_sentence, pos_sentence, technical_sentence)

    #3. make indefinite articles agree
    # while 'indefinite-article' in pos_sentence:
    #     new_determiner = self.make_article_agree(base_sentence[pos_sentence.index('indefinite-article')+1])
    #     base_sentence[pos_sentence.index('indefinite-article')] = new_determiner
    #     pos_sentence[pos_sentence.index('indefinite-article')] = 'determiner'


def route_nouns(diagram, bare_sentence, sentence):
    # import ipdb; ipdb.set_trace(context=20)
    while 'det' in diagram:
        # find all determiners and their following nouns for pluralization
        determiner_index = diagram.index('det')
        if "plur" in sentence[determiner_index]["fields"]["attributes"]:
            noun_index = -1
            for i in range(determiner_index, len(diagram)-determiner_index-1):
                if diagram[i] == "noun":
                    noun_index = i
                    break
            if noun_index >= 0:
                bare_sentence[noun_index] = pluralize_noun(sentence[noun_index])
                diagram[noun_index] = 'noun-inflected'
        diagram[determiner_index] = 'determiner-done'

    print(diagram)
    for i in range(len(diagram)):
        if '-done' in diagram[i]:
            diagram[i] = diagram[i][:-5]
        elif '-inflected' in diagram[i]:
            diagram[i] = diagram[i][:-10]
    print(diagram)
    return bare_sentence

def route_verbs(base_sentence, pos_sentence, technical_sentence):
    for i in range(len(pos_sentence)):
        if pos_sentence[i][:4] == 'verb':
            pos_sentence[i] = 'verb'
    while 'verb' in pos_sentence:
        # find all verbs and their preceding subjects and determiners
        verb_index = pos_sentence.index('verb')
        for i in range(verb_index, -1, -1):
            if pos_sentence[i] in ['determiner', 'indefinite-article', 'nominative-pronoun', 'possessive-pronoun', 'proper-noun']:
                determiner_index = i
                break
        for i in range(verb_index, -1, -1):
            if pos_sentence[i] in ['noun', 'nominative-pronoun', 'proper-noun']:
                subject_index = i
                break
        base_sentence[verb_index] = do_verb(
            technical_sentence[subject_index],
            technical_sentence[verb_index],
            technical_sentence[determiner_index].plural,
        )
        pos_sentence[verb_index] = 'verb-conjugated'

def make_article_agree(self, word):
    #
    # fix things like "an uniform" unicycle etc.
    #
    if word[0] in ['a', 'e', 'i', 'o', 'u']:
        if word[:3] not in ['uni',]:
            return 'an'
        else:
            return 'a'
    else:
        return 'a'


def pluralize_noun(noun):
    # take into account uncount and pluruncount
    if "plural" in noun["fields"]["inflections"]:
        noun = noun["fields"]["inflections"]["plural"]
    else:
        noun = noun["fields"]["inflections"]["base"]
        if noun[-2:] in ['ey', 'ay',]:
            noun = noun+'s'
        elif noun[-1] in ['y',]:
            noun = noun[:-1]+'ies'
        elif noun[-2:] in ['ss', 'ch',]:
            noun = noun+'es'
        elif noun[-1] in ['s',]:
            noun = noun+'ses'
        else:
            noun = noun+'s'
    return noun


def do_verb(subject, verb, is_plural):
    tense = random.choice([
        'present',
        'simple_past',
    ])

    if verb.base == 'be':
        return conjugate_for_be(subject, tense, is_plural)

    if tense == 'present':
        return conjugate_for_present(subject, verb, tense, is_plural)
    elif tense == 'simple_past':
        return conjugate_for_simple_past(verb)


def conjugate_for_present(subject, verb, tense, is_plural):
    if is_plural:
        return verb.base
    else:
        if subject.base not in ['i', 'you', 'we', 'they',]:
            if verb.present3s:
                return verb.present3s
            else:
                if verb.base[-1] == 'y' and verb.base[-2:] != 'ey':
                    return verb.base[:-1] + 'ies'
                elif verb.base[-1] == 'x':
                    return verb.base + 'es'
                elif verb.base[-2:] in ['sh', 'ch', 'ss']:
                    return verb.base + 'es'
                else:
                    return verb.base + 's'
        else:
            return verb.base


def conjugate_for_simple_past(verb):
    if verb.past:
        return verb.past
    else:
        if verb.base[-1] == 'e':
            return verb.base + 'd'
        elif verb.base[-2:] in ['ey', 'ay',]:
            return verb.base + 'ed'
        elif verb.base[-1] == 'y':
            return verb.base[:-1] + 'ied'
        else:
            return verb.base + 'ed'


def conjugate_for_be(subject, tense, is_plural):
    if is_plural:
        new_verb = BE[tense]['plural']
    else:
        if subject.base not in ['i', 'you',]:
            new_verb = BE[tense]['it']
        else:
            new_verb = BE[tense][subject.base]

    return new_verb
