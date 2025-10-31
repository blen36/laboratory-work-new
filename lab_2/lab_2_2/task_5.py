def cache(func):
    cached_results = {}

    def wrapper(*args):
        if args in cached_results:
            print(f"Берём из кэша для {args}")
            return cached_results[args]
        else:
            print(f"Вычисляем для {args}")
            result = func(*args)
            cached_results[args] = result
            return result

    return wrapper


@cache
def my_func(a, b):
    print(f"Считаем {a} * {b}...")
    return a * b

while True:
    print("\nВведите два числа для умножения (или 'q' для выхода):")

    a_input = input("Первое число: ")
    if a_input.lower() == 'q':
        print("Выход из программы...")
        break

    b_input = input("Второе число: ")
    if b_input.lower() == 'q':
        print("Выход из программы...")
        break

    a = int(a_input)
    b = int(b_input)

    result = my_func(a, b)
    print(f"Результат: {result}")