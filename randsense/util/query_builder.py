# categories: {'adv', 'conj', 'pron', 'aux', 'adj', 'verb', 'noun', 'det',
# 'modal', 'prep'}

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
    if specific_type:
        if ":" in specific_type:
            attribute, value = specific_type.split(":")
            kwargs[f"attributes__{attribute}__contains"] = value
        else:
            kwargs[f"attributes__{specific_type}__isnull"] = False
    elif specific_word:
        kwargs["base"] = specific_word
    return klass.objects.filter(**kwargs)
