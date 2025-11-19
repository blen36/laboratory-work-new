import pytest
from functions import *

class TestCountWords:
    def test_count_words_basic(self):
        assert count_words("hello world") == 2
        assert count_words("Python is awesome") == 3

    def test_count_words_empty(self):
        assert count_words("") == 0
        assert count_words("   ") == 0

    def test_count_words_multiple_spaces(self):
        assert count_words("  hello   world  ") == 2
        assert count_words("   one   two   three   ") == 3

    def test_count_words_single_word(self):
        assert count_words("hello") == 1
        assert count_words("  hello  ") == 1

    def test_count_words_with_punctuation(self):
        assert count_words("Hello, world! How are you?") == 5
        assert count_words("Python... is... great!!!") == 3

class TestFindUnique:
    def test_basic_case(self):
        assert unique_elements([1, 2, 2, 3, 4, 4, 5]) == [1, 2, 3, 4, 5]

    def test_strings(self):
        assert unique_elements(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]

    def test_all_unique(self):
        assert unique_elements([1, 2, 3]) == [1, 2, 3]

    def test_all_same(self):
        assert unique_elements([1, 1, 1, 1]) == [1]

    def test_empty_list(self):
        assert unique_elements([]) == []

class TestIsPalindrome:
    def test_word_palindromes(self):
        assert is_palindrome("racecar") == True
        assert is_palindrome("level") == True
        assert is_palindrome("hello") == False

    def test_phrase_palindromes(self):
        assert is_palindrome("A man a plan a canal Panama") == True

    def test_number_palindromes(self):
        assert is_palindrome(12321) == True
        assert is_palindrome(12345) == False

    def test_case_insensitive(self):
        assert is_palindrome("Racecar") == True
        assert is_palindrome("Level") == True

    def test_single_character(self):
        assert is_palindrome("a") == True
        assert is_palindrome("1") == True

class TestAreAnagrams:
    def test_basic_anagrams(self):
        assert are_anagrams("listen", "silent") == True
        assert are_anagrams("hello", "world") == False

    def test_case_insensitive(self):
        assert are_anagrams("Listen", "Silent") == True

    def test_with_spaces(self):
        assert are_anagrams("school master", "the classroom") == True

    def test_different_length(self):
        assert are_anagrams("test", "testing") == False

    def test_same_word(self):
        assert are_anagrams("python", "python") == True

    def test_empty_strings(self):
        assert are_anagrams("", "") == True

class TestCombineDicts:
    def test_basic_combination(self):
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}
        expected = {"a": 1, "b": 2, "c": 3, "d": 4}
        assert combine_dicts(dict1, dict2) == expected

    def test_overwrite_values(self):
        dict1 = {"a": 1, "b": 2}
        dict2 = {"b": 3, "c": 4}
        expected = {"a": 1, "b": 3, "c": 4}
        assert combine_dicts(dict1, dict2) == expected

    def test_empty_dicts(self):
        assert combine_dicts({}, {}) == {}
        assert combine_dicts({"a": 1}, {}) == {"a": 1}
        assert combine_dicts({}, {"b": 2}) == {"b": 2}

    def test_nested_dicts(self):
        dict1 = {"a": {"x": 1}, "b": 2}
        dict2 = {"a": {"y": 2}, "c": 3}
        expected = {"a": {"y": 2}, "b": 2, "c": 3}
        assert combine_dicts(dict1, dict2) == expected

