input_list = input("Введите список: ").split()
original_list = input_list.copy()

for el in original_list:
    if input_list.count(el) > 1:
        while el in input_list:
            input_list.remove(el)

print(f"Список без дубликатов: {input_list}")
