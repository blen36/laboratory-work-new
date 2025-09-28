def flatten(lst):
    i = 0
    while i < len(lst):
        if isinstance(lst[i], list):
            nested_list=lst[i]
            lst[i: i+1]=nested_list
        else:
            i += 1
    if any(isinstance(i, list) for i in lst):
        flatten(lst)
lst=[[1,2,3],[4,5,6],[7,8,9]]
print(f"Лист до: {lst}")
flatten(lst)
print(f"Лист после: {lst}")