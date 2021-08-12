# categories: {'adv', 'conj', 'pron', 'aux', 'adj', 'verb', 'noun', 'det',
# 'modal', 'prep'}

# No adj, conj, prep, modal, aux
LOOKUP_FIELDS = {
    "Pronoun": "type",
    "Determiner": "variants",
    "Noun": "variants",
    "Adverb": "modification",
}


def get_category_and_type(category):
    # TODO: Cannot currently mix : and *
    if ":" in category:
        split = category.split(":", 1)
        split.append(None)
        return split  # ["verb", "intran", None]
    elif "*" in category:
        # If we want an exact match, we have to return ["category", None, "word"]
        split = category.split("*", 1)
        split[1:1] = [None]
        split[-1] = split[-1].replace("&", " ")
        return split  # ["noun", None, "praying mantis"]
    else:
        return category, None, None


def get_query_for_category(klass, specific_type=None, specific_word=None):
    kwargs = {}
    # Verbs are special; their tags are attributes
    if klass.__name__ == "Verb" and specific_type:
        if ":" in specific_type:
            specific_type, attribute = specific_type.split(":")
            kwargs[f"attributes__{specific_type}__contains"] = attribute
        else:
            kwargs[f"attributes__{specific_type}__isnull"] = False
    elif specific_type:
        kwargs[f"attributes__{LOOKUP_FIELDS[klass.__name__]}__contains"] = specific_type
    elif specific_word:
        kwargs["base"] = specific_word
    return klass.objects.filter(**kwargs)
