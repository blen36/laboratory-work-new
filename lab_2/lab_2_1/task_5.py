word1=input("Введите 1-ое слово: ").lower()
word2=input("Введите 2-ое слово: ").lower()
if sorted(word1) == sorted(word2):
    print("True")
else:
    print("False")