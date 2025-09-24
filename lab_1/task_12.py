print("Тарифный план: 60 мин. разговора, 30 смс, 1ГБ трафика\nЦена 24,99 руб. в месяц")
print("Каждая дополнительная минута стоит 0,89 руб., каждое дополнительное сообщение –0,59 руб., каждый дополнительный Мб – 0,79 руб.")

minutes=int(input("Введите количество израсходованных за месяц минут разговора: "))
sms=int(input("Введите количество израсходованных за месяц смс: "))
traffic=int(input("Введите количество израсходованного за месяц трафика в МБ: "))
print('-'*40)
if minutes>60:
    sumDopMin=(minutes-60)*0.89
    print(f"Доп.услуги за минуты разговора: {sumDopMin:.2f} руб.")
else: sumDopMin=0
if sms>30:
    sumDopSms=(sms-30)*0.59
    print(f"Доп.услуги за смс: {sumDopSms:.2f} руб.")
else: sumDopSms=0
if traffic>1000:
    sumDopTraffic=(traffic-1000)*0.79
    print(f"Доп.услуги за трафик: {sumDopTraffic:.2f} руб.")
else: sumDopTraffic=0

if minutes<60 and sms<30 and traffic<1000:
    print("Общая сумма: 24,99 руб.")

if minutes>60 or sms>30 or traffic>1000:
    totalSum=24.99+sumDopMin+sumDopSms+sumDopTraffic+(24.99+sumDopMin+sumDopSms+sumDopTraffic)*0.02
    print(f"Общая сумма: {totalSum:.2f}")
print('-'*40)