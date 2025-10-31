def merge_dicts(d1, d2):
    for key, value in d2.items():
        if (
            key in d1
            and isinstance(d1[key], dict)
            and isinstance(value, dict)
        ):
            merge_dicts(d1[key], value)
        else:
            d1[key] = value
    return d1

dict_a = {"a": 1, "b": {"c": 1, "f": 4}, "list": [1, 2, 3]}
dict_b = {"d": 1, "b": {"c": 2, "e": 3}}

merge_dicts(dict_a, dict_b)
print(f"Слияние двух словарей: {dict_a}")
