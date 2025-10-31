str = input("Введите строку: ").lower().split()
d = {}
for word in str:
    if word in d:
        d[word] += 1
    else:
        d[word] = 1

print(d)
print(len(set(str)))
