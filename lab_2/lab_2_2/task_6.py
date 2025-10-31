def unique(lst):
    result = []

    flat = []
    for item in lst:
        if isinstance(item, list):
            flat.extend(unique(item))
        else:
            flat.append(item)

    for item in flat:
        if item not in result:
            result.append(item)

    return result

lst = [1, 2, 3, [4, 3, 1], 5, [6, [7, [10], 8, [9, 2, 3]]]]
print(f"Лист до: {lst}")
print(f"Только уникальные элементв: {unique(lst)}")
