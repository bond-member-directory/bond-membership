def clean_object(obj):
    new_obj = {}

    obj.pop("attributes", None)
    for key, value in obj.items():
        new_key = key.replace("__c", "").replace("__r", "").replace("_", "")
        new_key = new_key[:1].lower() + new_key[1:] if new_key else ""
        new_obj[new_key] = value
    return new_obj
