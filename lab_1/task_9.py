#Введите строку. Проверьте, является ли она корректным IP-адресом (формат
#должен быть ХХХ.ХХХ.ХХХ.ХХХ, где ХХХ – число от 0 до 255).
ip=input("Введите строку: ")
parts=ip.split(".")
if len(parts)==4 and all(part.isdigit() and 0<=int(part)<=255 for part in parts):
    print("Корректный IP-адрес")
else:
    print("Некорректный IP-адрес")