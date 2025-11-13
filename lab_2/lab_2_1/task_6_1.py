input_list = input("Введите список: ").split()

unique_list = []

for el in input_list:
    if el not in unique_list:
        unique_list.append(el)
print(unique_list)


