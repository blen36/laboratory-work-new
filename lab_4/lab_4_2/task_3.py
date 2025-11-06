import numpy as np

A = np.array([
    [-2, -8.5, -3.4, 3.5],
    [0, 2.4, 0, 8.2],
    [2.5, 1.6, 2.1, 3],
    [0.3, -0.4, -4.8, 4.6]
])

B = np.array([-1.88, -3.28, -0.5, -2.83])

print(f"Матрица коэффициентов A:\n{A}")
print(f"Вектор правых частей B: {B}")

det_A = np.linalg.det(A)
print(f"Определитель матрицы A: {det_A:.4f}")

if abs(det_A) < 1e-10:
    print("Матрица A вырождена, решение невозможно")
else:
    A_inv = np.linalg.inv(A)
    X = A_inv @ B

    print("Обратная матрица A^(-1):")
    print(A_inv)

    print("Решение системы X = A^(-1) * B:")
    print(f"x1 = {X[0]:.1f}")
    print(f"x2 = {X[1]:.1f}")
    print(f"x3 = {X[2]:.1f}")
    print(f"x4 = {X[3]:.1f}")

    print(f"Вектор-решение (округлено до одного знака):")
    print(np.round(X, 1))