import matplotlib.pyplot as plt
import numpy as np

x_degrees = np.linspace(-360, 360, 1000)
x_rad = np.radians(x_degrees)
f_x = np.exp(np.cos(x_rad))+np.log(np.cos(0.6*x_rad)**2+1)*np.sin(x_rad)
h_x = -np.log((np.cos(x_rad)+np.sin(x_rad))**2+2.5)+10

plt.plot(x_degrees, f_x, label='f(x)', color='r', linewidth=2)
plt.plot(x_degrees, h_x, label='h(x)', color='b', linewidth=2)

plt.xlabel('x, deg')
plt.ylabel('y')
plt.title('Графики функции f(x) и h(x)')

plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
