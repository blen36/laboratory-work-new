inputStr=input("Введите текст: ").split()
wordCount={}
for word in inputStr:
    wordLower=word.lower()
    if wordLower in wordCount:
        wordCount[wordLower]+=1
    else:
        wordCount[wordLower]=1
print(f"Словарь будет таким: {wordCount}")

uniqueWordCount=0
for word in wordCount:
    if wordCount[word] == 1:
        uniqueWordCount += 1
print(f"Количество уникальных слов: {uniqueWordCount}")