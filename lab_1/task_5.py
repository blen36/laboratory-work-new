digit=int(input("Введите число: "))
if digit%7 == 0:
    print("Магическое число")
else:
    sum_digits=0
    while digit>0:
        sum_digits+=digit%10
        digit//=10
    print(sum_digits)
    #проверка ветки