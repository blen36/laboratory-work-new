def cache(func):
    cached_results = {}

    def wrapper(*args):
        if args in cached_results:
            print(f"Берём из кэша для {args}")
            return cached_results[args]
        else:
            print(f"Вычисляем заново для {args}")
            result = func(*args)
            cached_results[args] = result
            return result

    return wrapper

@cache
def my_func(a, b):
    print(f"Считаем {a} * {b}...")
    return a * b


print(my_func(2, 3))
print(my_func(2, 3))
print(my_func(4, 5))
print(my_func(2, 3))
