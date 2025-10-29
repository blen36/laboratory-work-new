def transp_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = []

    for row in range(rows):
        for col in range(cols):
            if len(transposed) <= col:
                transposed.append([])
            transposed[col].append(matrix[row][col])
    return transposed

def input_matrix():
    print("Введите размеры матрицы:")
    rows = int(input("Количество строк: "))
    cols = int(input("Количество столбцов: "))

    matrix = []
    print(f"\nВведите матрицу {rows}×{cols} (числа через пробел):")

    for i in range(rows):
        row_input = input(f"Строка {i + 1}: ")
        row = list(map(int, row_input.split()))
        matrix.append(row)

    return matrix

my_matrix = input_matrix()
transposed = transp_matrix(my_matrix)

print("\nИсходная матрица:")
for row in my_matrix:
    print(row)

print("\nТранспонированная матрица:")
for row in transposed:
    print(row)