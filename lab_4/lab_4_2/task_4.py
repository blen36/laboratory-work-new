import numpy as np
from scipy import integrate

def integrand1(x):
    return np.sin(x) / (np.cos(x)**2 + 1)

a = np.pi / 2
b = np.pi

result1, error1 = integrate.quad(integrand1, a, b)

print("=== Определённый интеграл ===")
print(f"Результат: {result1:.12f}")
print(f"Погрешность: {error1:.2e}\n")

def integrand2(y, x):
    return np.sin(x) * np.cos(y)

x0, x1 = 0, np.pi
y0 = lambda x: 0
y1 = lambda x: np.pi / 2

result2, error2 = integrate.dblquad(integrand2, x0, x1, y0, y1)

print("=== Двойной интеграл ===")
print(f"Результат: {result2:.12f}")
print(f"Погрешность: {error2:.2e}")
