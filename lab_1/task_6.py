pressure = float(input("Введите давление в Паскалях: "))
volume = float(input("Введите объем в м^3: "))
temperature =float(input("Введите температуру в Кельвинах: "))

R=8.31
n=(pressure*volume)/(R*temperature)
print(f"Количество газа в молях: {n:.2f}")