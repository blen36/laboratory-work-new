numbers = [float(x) for x in input("Введите список целых чисел через пробел: ").split()]
uniqueDigits = []
repeatedDigits = []
chet = []
nechet = []
negative=[]
isFloat=[]
sum=0
for digit in numbers:
    if numbers.count(digit) == 1:
        uniqueDigits.append(digit)
    else:
        if digit not in repeatedDigits:
            repeatedDigits.append(digit)

    if digit.is_integer():
        if digit % 2 == 0:
            if digit not in chet:
                chet.append(digit)
        else:
            if digit not in nechet:
                nechet.append(digit)
    else:
        if digit not in isFloat:
            isFloat.append(digit)

    if digit<0:
        if digit not in negative:
            negative.append(digit)
    if digit%5==0:
        sum+=digit

print(f"Уникальные числа: {uniqueDigits}")
print(f"Повторяющиеся числа: {repeatedDigits}")
print(f"Четные числа: {chet}")
print(f"Нечетные числа: {nechet}")
print(f"Отрицательные числа: {negative}")
print(f"Числа с плавающей точкой: {isFloat}")
print(f"Сумму всех чисел, кратных 5: {sum}")
print(f"Максимальное число: {max(numbers)}")
print(f"Минимальное число: {min(numbers)}")