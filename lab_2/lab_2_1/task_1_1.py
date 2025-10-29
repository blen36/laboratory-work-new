str = input("Введите строку: ").lower().split()
d = {}
for word in str:
    if word in d:
        d[word] += 1
    else:
        d[word] = 1

print(d)
uniqueWordCount=0
for word in d:
    if d[word] == 1:
        uniqueWordCount += 1
print(f"Количество уникальных слов: {uniqueWordCount}")
#или так uniqueWordCount = sum(1 for count in d.values() if count == 1)
