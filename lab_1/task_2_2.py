str = input("Введите строку(на английском): ").lower()
result=str.replace("a","").replace("o","").replace("e","")\
    .replace("i","").replace('u','').replace('y','')
print(result)