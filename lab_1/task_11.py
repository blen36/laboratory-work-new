date=input("Введите дату рождения(ДД.ММ): ")
date=date.replace('/','.')
parts=date.split(".")
if len(parts)!=2:
    print("Введите дату в формате ДД.ММ")
day=int(parts[0])
month=int(parts[1])
if (month == 12 and day >= 22) or (month == 1 and day <= 20):
    print("Козерог")
elif (month == 1 and day >= 21) or (month == 2 and day <= 19):
    print ("Водолей")
elif (month == 2 and day >= 20) or (month == 3 and day <= 20):
    print ("Рыбы")
elif (month == 3 and day >= 21) or (month == 4 and day <= 20):
    print ("Овен")
elif (month == 4 and day >= 21) or (month == 5 and day <= 21):
    print ("Телец")
elif (month == 5 and day >= 22) or (month == 6 and day <= 21):
    print ("Близнецы")
elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
    print ("Рак")
elif (month == 7 and day >= 23) or (month == 8 and day <= 21):
    print ("Лев")
elif (month == 8 and day >= 22) or (month == 9 and day <= 23):
    print ("Дева")
elif (month == 9 and day >= 24) or (month == 10 and day <= 23):
    print ("Весы")
elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
    print ("Скорпион")
elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
    print ("Стрелец")
else:
    print ("Неверная дата")