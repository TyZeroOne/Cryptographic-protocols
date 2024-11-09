import random

def generate_regular_graph(n, k):
    if (n * k) % 2 != 0:
        return "Невозможно создать регулярный граф: произведение n и k должно быть четным"
    if k >= n:
        return "Невозможно создать регулярный граф: степень вершины должна быть меньше числа вершин"
    graph = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(1, k // 2 + 1):
            neighbor = (i + j) % n
            graph[i][neighbor] = 1
            graph[neighbor][i] = 1  
    if k % 2 == 1:
        for i in range(n // 2):
            neighbor = (i + n // 2) % n
            graph[i][neighbor] = 1
            graph[neighbor][i] = 1
    
    return graph


def read_matrix_from_file(filename):
    with open(filename, 'r') as f:
        matrix = [list(map(int, line.split())) for line in f]
    return matrix

def write_matrix_to_file(matrix, filename):
    with open(filename, 'w') as f:
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')

def generate_permutation(matrix_size, p):
    permutation = list(range(matrix_size))
    random.shuffle(permutation) 
    while permutation == p:
        random.shuffle(permutation) 
    return permutation

def write_permutation_to_file(permutation, filename):
    with open(filename, 'w') as file:
        file.write(' '.join(map(str, permutation)) + '\n')

def read_permutation_from_file(filename):
    with open(filename, 'r') as file:
        permutation = list(map(int, file.readline().split()))
    return permutation

def apply_permutation(matrix, permutation):
    permuted_matrix = [[matrix[i][j] for j in permutation] for i in permutation]
    return permuted_matrix

def mix_permutation(permutation_1, permutation_2):
    new_permutation = [permutation_2[i] for i in permutation_1]
    return new_permutation

def print_graph(matrix):
    for row in matrix:
        print(" | ".join(f"{val:2}" for val in row))

def main():
    o = input("Введите 1 для генерации параметров\nВведите 2 для проверки доказательства\n")
    if o == "1":
        n = int(input("Введите количество вершин графа: "))
        degree = int(input("Введите степени вершин у графа: "))
        tmp = generate_regular_graph(n, degree)
        write_matrix_to_file(tmp, "matrix_G0.txt")  
        G0 = read_matrix_from_file("matrix_G0.txt")
        mas = list(range(0, len(G0)))
        tmp = generate_permutation(len(G0), mas)
        write_permutation_to_file(tmp, "secret_permutation.txt")
        p = read_permutation_from_file("secret_permutation.txt")
        G1 = apply_permutation(G0, p)
        write_matrix_to_file(G1, "matrix_G1.txt")
        h = generate_permutation(len(G0), p)
        write_permutation_to_file(h, "permutation.txt")
        H = apply_permutation(G1, h)
        write_matrix_to_file(H, "matrix_H.txt")
    elif o == "2":
        word = "-1"
        while word != "stop":
            word = input("Введите stop для остановки")
            k = random.randint(0, 1)
            if k == 1:
                H = read_matrix_from_file("matrix_H.txt")
                print("Граф H: ")
                print_graph(H)
                G1 = read_matrix_from_file("matrix_G1.txt")
                print("Граф G1: ")
                print_graph(G1)
                h = read_permutation_from_file("permutation.txt")
                print("Переданная перестановка: ", h)
                new_G1 = apply_permutation(G1, h)
                print("Перестановка графа G1: ")
                print_graph(new_G1)
                if H != new_G1:
                    print("Изоморфизм не доказан")
                    print(0)
                else:
                    print("Изоморфизм доказан")
                    print(1)
            else:
                p = read_permutation_from_file("secret_permutation.txt")
                h = read_permutation_from_file("permutation.txt")
                G0 = read_matrix_from_file("matrix_G0.txt")
                H = read_matrix_from_file("matrix_H.txt")
                print("Граф H: ")
                print_graph(H)
                print("Граф G0: ")
                print_graph(G0)
                l = mix_permutation(h, p)
                print("Переданная перестановка: ", l)
                new_G0 = apply_permutation(G0, l)
                print("Перестановка графа G0: ")
                print_graph(new_G0)
                if H != new_G0:
                    print("Изоморфизм не доказан")
                    print(0)
                else:
                    print("Изоморфизм доказан")
                    print(1)
        return
main()

