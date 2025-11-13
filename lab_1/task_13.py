import random

random_int=random.randint(1,100)
print(random_int)
print("Введите свои догатки: ")
while(True):
    guess=int(input())
    if guess==random_int:
        print("Вы угадали!")
        break
    else:
        if(guess>random_int):
            print("Меньше")
        elif(guess<random_int):
            print("Больше")