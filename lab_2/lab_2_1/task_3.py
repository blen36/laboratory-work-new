numbers=[int(x) for x in input("Введите список чисел: ").split()]
uniqueNumbers=[]
for number in numbers:
    if number not in uniqueNumbers:
        uniqueNumbers.append(number)
if len(uniqueNumbers)<2:
    print("В списке должно быть минимум 2 числа")
else:
    maxNumber = max(uniqueNumbers)
    secondMaxNumber = min(uniqueNumbers)
    for number in uniqueNumbers:
        if number > secondMaxNumber and number < maxNumber:
            secondMaxNumber = number
print("Все числа одинаковые, второго по величине нет" if secondMaxNumber==min(uniqueNumbers) else f"Второе по величине число: {secondMaxNumber}")
