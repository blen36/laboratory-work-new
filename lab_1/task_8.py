str_pal=input("Введите строку: ").lower().replace(" ", "")
is_pal=str_pal==str_pal[::-1]
print("Палиндром" if is_pal else "Не палиндром")