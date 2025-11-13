import  datetime

def log_calls(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with open(filename, 'a', encoding = 'utf-8') as f:
                f.write(f"{datetime.datetime.now()} - {func.__name__}(args={args}, kwargs={kwargs})\n")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_calls('log.txt')
def my_func(a,b):
    return a+b
@log_calls('log.txt')
def greet(name, greeting):
    return f"{greeting}, {name}!"

my_func(5,6)
greet("Irina", greeting = "Hello")
greet("Egor", greeting = "Hi")