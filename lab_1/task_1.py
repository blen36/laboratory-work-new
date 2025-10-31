print("Введите ваши данные(ФИО):")
last_name=input("Фамилия: ").strip()
first_name=input("Имя: ")
patronymic=input("Отчество: ")

if not last_name or not first_name or not patronymic:
    print("Вы ввели не все данные")
    exit()
last_name=last_name[0].upper()+last_name[1:].lower()
print(f"{last_name} {first_name[0].upper()}.{patronymic[0].upper()}.")