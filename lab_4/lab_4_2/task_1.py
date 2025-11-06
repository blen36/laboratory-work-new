import numpy as np

months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
          'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
expenses_list = np.random.randint(20, 56, size = 12)
expenses_per_month = np.array(expenses_list)

winter_indexes = [0,1,11]
summer_indexes = [5,6,7]

winter_pare = np.sum(expenses_per_month[winter_indexes])
summer_pare = np.sum(expenses_per_month[summer_indexes])

print(expenses_per_month)
print(f"Зимние месяцы: {[months[i] for i in winter_indexes]}")
print(f"Сумма: {winter_pare} byn.")
print(f"Летние месяцы: {[months[i] for i in summer_indexes]}")
print(f"Сумма: {summer_pare} byn.")

if winter_pare > summer_pare:
    difference = winter_pare - summer_pare
    print(f"Зимой на {difference} byn больше.")
elif summer_pare > winter_pare:
    difference = summer_pare - winter_pare
    print(f"Летом на {difference} byn больше.")
else:
    print("Зимой и летом поровну.")

max_expense = np.max(expenses_per_month)
# Находим ВСЕ месяцы с максимальными расходами (на случай одинаковых значений)
max_months_indexes = np.where(expenses_per_month == max_expense)[0]   # +1 потому что месяцы с 1

print(f"Максимальные расходы: {max_expense} byn.")
print("Месяцы с максимальными расходами:", [months[i] for i in max_months_indexes])

# Дополнительно: все месяцы с расходами выше среднего
average_expense = np.mean(expenses_per_month)
above_average_indexes = np.where(expenses_per_month > average_expense)[0]
print(f"Средние расходы: {average_expense:.2f} руб.")
print("Месяцы с расходами выше среднего:", [months[i] for i in above_average_indexes])
