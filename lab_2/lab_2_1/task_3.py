numbers=[int(x) for x in input("Введите список чисел: ").split()]
uniqueNumbers=[]
for number in numbers:
    if number not in uniqueNumbers:
        uniqueNumbers.append(number)
if len(uniqueNumbers)<2:
    print("В списке должно быть минимум 2 числа")
else:
    maxNumber = max(uniqueNumbers)
    secondMaxNumber = -10**18
    for number in uniqueNumbers:
        if number > secondMaxNumber and number < maxNumber:
            secondMaxNumber = number
print("Все числа одинаковые, второго по величине нет" if secondMaxNumber==-10**18 else f"Второе по величине число: {secondMaxNumber}")
