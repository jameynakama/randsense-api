# categories: {'adv', 'conj', 'pron', 'aux', 'adj', 'verb', 'noun', 'det',
# 'modal', 'prep'}

# No adj, conj, prep, modal, aux
LOOKUP_FIELDS = {
    "Pronoun": "type",
    "Determiner": "variants",
    "Noun": "variants",
    "Adverb": "modification"
}


def get_category_and_type(category):
    if ":" in category:
        return category.split(":", 1)
    else:
        return category, None


def get_query_for_category(klass, specific_type=None):
    kwargs = {}
    # Verbs are special; their tags are attributes
    if klass.__name__ == "Verb" and specific_type:
        kwargs[f"attributes__{specific_type}__isnull"] = False
    elif specific_type:
        kwargs[f"attributes__{LOOKUP_FIELDS[klass.__name__]}__contains"] = specific_type
    return klass.objects.filter(**kwargs)
