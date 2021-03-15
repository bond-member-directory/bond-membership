def clean_object(obj):
    new_obj = {}

    obj.pop("attributes", None)
    for key, value in obj.items():
        new_key = key.replace("__c", "").replace("__r", "").replace("_", "")
        new_key = new_key[:1].lower() + new_key[1:] if new_key else ""
        new_obj[new_key] = value
    return new_obj


def to_dotted(d, parent=None, separator="."):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from to_dotted(v, k, separator=separator)
        elif parent:
            yield (separator.join((str(parent), str(k))), v)
        else:
            yield (k, v)
