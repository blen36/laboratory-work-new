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

my_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = transp_matrix(my_matrix)

print("Исходная матрица:")
for row in my_matrix:
    print(row)

print("\nТранспонированная матрица:")
for row in transposed:
    print(row)