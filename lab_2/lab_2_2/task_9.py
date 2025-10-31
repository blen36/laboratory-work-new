def type_check(*types):
    def decorator(func):
        def wrapper(*args):
            for arg, t in zip(args, types):
                if not isinstance(arg, t):
                    raise TypeError("Неверный тип аргумента")
            return func(*args)
        return wrapper
    return decorator


@type_check(int, int)
def add(a, b):
    return a + b

print(add(3, 4))

