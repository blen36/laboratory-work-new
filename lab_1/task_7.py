second=int(input("Введите количество секунд: "))
minute=second//60
second_remainder=second%60

if minute % 10 == 1 and minute % 100 != 11: # 1, 21, 31 минута (но не 11)
    minute_str = "минута"
elif 2 <= minute % 10 <= 4 and (minute % 100 < 10 or minute % 100 >= 20):
    minute_str = "минуты"  # 2-4, 22-24, 32-34 минуты
else:
    minute_str = "минут"  # 0, 5-20, 25-30, 35-40 минут

if second_remainder % 10 == 1 and second_remainder % 100 != 11:
    second_str = "секунда"
elif 2 <= second_remainder % 10 <= 4 and (second_remainder % 100 < 10 or second_remainder % 100 >= 20):
    second_str = "секунды"
else:
    second_str = "секунд"

print(f"{second} секунд = {minute} {minute_str} {second_remainder} {second_str}")