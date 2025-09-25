str_input = input("Введите строку: ")
newstr = ""
i = 0

while i < len(str_input):
    char = str_input[i]
    count = 1

    while i + 1 < len(str_input) and str_input[i + 1] == char:
        count += 1
        i += 1

    newstr += char + str(count)
    i += 1

print(newstr)