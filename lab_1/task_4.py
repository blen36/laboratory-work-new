sum=int(input("Введите сумму в рублях: "))
if sum<0:
    print("Сумма не может быть отрицательной")
else:
    print(f"Сумма: {sum} в руб.")
    print("Для размена требуется: ")
    banknotes_100=sum//100
    sum%=100
    banknotes_50=sum//50
    sum%=50
    banknotes_20=sum//20
    sum%=20
    banknotes_10=sum//10
    sum%=10
    banknotes_5=sum//5
    sum%=5
    coins_2=sum//2
    sum%=2
    coins_1=sum

    if banknotes_100>0: print(f"Купюр по 100 руб. : {banknotes_100}")
    if banknotes_50>0:print(f"Купюр по 50 руб. : {banknotes_50}")
    if banknotes_20>0:print(f"Купюр по 20 руб. : {banknotes_20}")
    if banknotes_10>0:print(f"Купюр по 10 руб. : {banknotes_10}")
    if banknotes_5>0:print(f"Купюр по 5 руб. : {banknotes_5}")
    if coins_2>0:print(f"Монет по 2 руб. : {coins_2}")
    if coins_1>0:print(f"Купюр по 1 руб. : {coins_1}")