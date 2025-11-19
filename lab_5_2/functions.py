# ЗАДАНИЕ 1
def count_words(sentence):
    if not sentence or not sentence.strip():
        return 0
    words = sentence.strip().split()
    return len(words)

# ЗАДАНИЕ 2
def unique_elements(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# ЗАДАНИЕ 3
def is_palindrome(word):
    text = str(word).lower().replace(' ','')
    return text == text[::-1]

# ЗАДАНИЕ 4
def are_anagrams(word1, word2):
    word1 = word1.lower().replace(" ", "")
    word2 = word2.lower().replace(" ", "")
    return sorted(word1) == sorted(word2)

# ЗАДАНИЕ 5
def combine_dicts(dict1, dict2):
    result = dict1.copy()
    result.update(dict2)
    return result
