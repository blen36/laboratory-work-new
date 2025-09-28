import time
def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        miliseconds = (end - start) * 1000
        print(f"Функция {func.__name__} выплнялась {miliseconds}мл")
        return result
    return wrapper

@timing
def function(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total

print(f"Результат: {function(10000)}")