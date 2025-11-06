import matplotlib.pyplot as plt
import numpy as np

x1 = np.linspace(-10, -3.1, 100)
x2 = np.linspace(-2.9, 2.9, 100)
x3 = np.linspace(3.1, 10, 100)

y1 = 5/(x1**2 - 9)
y2 = 5/(x2**2 - 9)
y3 = 5/(x3**2 - 9)

plt.figure(figsize=(10, 6))
plt.plot(x1, y1, 'r-', linewidth=2, label='f(x)')
plt.plot(x2, y2, 'r-', linewidth=2)
plt.plot(x3, y3, 'r-', linewidth=2)


plt.axvline(x=-3, color='gray', linestyle='--', alpha=0.7, label='Вертикальные асимптоты')
plt.axvline(x=3, color='gray', linestyle='--', alpha=0.7)

plt.xlabel('x')
plt.ylabel('y')
plt.title('График функции f(x) = 5/(x² - 9)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()