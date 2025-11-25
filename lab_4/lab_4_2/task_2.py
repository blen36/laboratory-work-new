import numpy as np

length = input("Введите длины участков через пробел: ").strip().split()
velocity = input("Введите скорости на участках через пробел: ").strip().split()
k = int(input("Введите номер участка въезда (k): ").strip())
p = int(input("Введите номер участка выезда (p): ").strip())

lengths = np.array(length, dtype=float)
velocities = np.array(velocity, dtype=float)

selected_lengths = lengths[k-1:p]
selected_velocities = velocities[k-1:p]

S = np.sum(selected_lengths)
T = np.sum(selected_lengths / selected_velocities)
V = S / T

print(f"Длина пути: {S:.2f}")
print(f"Время в пути: {T:.2f}")
print(f"Средняя скорость: {V:.2f}")