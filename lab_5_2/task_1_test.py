from task_1 import count_words
import pytest

def test_count_words_basic():
    """Тест обычного предложения"""
    assert count_words("hello world") == 2
    assert count_words("Python is awesome") == 3

def test_count_words_empty():
    """Тест пустых строк"""
    assert count_words("") == 0
    assert count_words("   ") == 0

def test_count_words_multiple_spaces():
    """Тест с множественными пробелами"""
    assert count_words("  hello   world  ") == 2
    assert count_words("   one   two   three   ") == 3

def test_count_words_single_word():
    """Тест одного слова"""
    assert count_words("hello") == 1
    assert count_words("  hello  ") == 1

def test_count_words_with_punctuation():
    """Тест со знаками препинания"""
    assert count_words("Hello, world! How are you?") == 5
    assert count_words("Python... is... great!!!") == 3

def test_count_words_numbers():
    """Тест с числами"""
    assert count_words("1 2 3 4 5") == 5
    assert count_words("Python 3.11 is released") == 4

def test_count_words_mixed_case():
    """Тест с разным регистром"""
    assert count_words("Hello WORLD test") == 3
    assert count_words("UPPER lower Mixed") == 3

def test_count_words_special_characters():
    """Тест со специальными символами"""
    assert count_words("@user #tag $price") == 3
    assert count_words("test1 test2 test3") == 3