str = input("Введите строку(на английском): ")
result=str.replace("a","").replace("o","").replace("e","")\
    .replace("i","").replace('u','').replace('y','').replace('A','')\
    .replace('O','').replace('E','').replace('I','').replace('Y','')\
    .replace('U','')
print(result)