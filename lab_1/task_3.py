password=input("Введите пароль: ")
if len(password)<16:
    print("Пароль слишком короткий")
elif password.isdigit() or password.isalpha():
    print("Слабый пароль")
else:
    print("Надежный пароль")