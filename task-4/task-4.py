import random
import sympy

def length(a):
    b = pow(10, a - 1)
    c = pow(10, (a)) - 1
    return b, c

def generate_prime(limit):
    a, b = length(limit)
    prime_candidate = random.randint(a, b)
    while not sympy.isprime(prime_candidate):
        prime_candidate = random.randint(a, b)
    return prime_candidate

def find_generator(p):
    q = random.randint(2, (p - 1) // 2)
    while (p - 1) % q != 0 or not sympy.isprime(q):
        q = random.randint(2, p - 1)
    return q


def write_to_file(files, message):
    with open(files, 'w') as file:
        file.write(','.join(map(str, message)))

def open_file(files):
    with open(files, 'r') as file:
        data = tuple(map(str, file.read().split(',')))
    return data

def generate_params(bits):
    p = generate_prime(bits)
    q = find_generator(p)
    while q is None:
        p = generate_prime(bits)
        q = find_generator(p)
    for i in range(2, p - 1):
        if pow(i, q, p) == 1:
            g = i
    write_to_file("public.txt", (p, q, g))

def gen_key():
    p, q, g = open_file('public.txt')
    w = random.randint(1, q - 1)
    y = pow(g, -w, p)
    write_to_file("public_Alice.txt", (y, ))
    write_to_file("private_Alice.txt", (w, ))

def gen_Alice(e):
    p, q, g = open_file('public.txt')
    r = random.randint(2, q - 1)
    x = pow(g, r, p)
    w = open_file("private_Alice.txt")[0]
    s = (r + w * e) % q
    write_to_file("Alice_to_Bob.txt", (x, s))

def main():
    k = int(input("Введите режим работы:\n1 - Генерация ключей\n2 - Отправляет Боб\n3 - Отправляет Алиса\n4 - Проверка\n"))
    if k == 1:
        bits = int(input("Введите число бит: "))
        generate_params(bits)
        gen_key()
    if k == 2:
        t = int(input("Введите параметр безопасности: "))
        e = random.randint(0, int(pow(2, t)) - 1)
        write_to_file("Bob_to_Alice.txt", (e, ))
    if k == 3:
        e = open_file("Bob_to_Alice.txt")[0]
        gen_Alice(e)
    if k == 4:    
        y = open_file("public_Alice.txt")[0]
        p, q, g = open_file('public.txt')
        x, s = open_file("Alice_to_Bob.txt")
        if x == pow(g, s, p) * pow(y, e, p):
            print("Проверка успешена")
            return
        else:
            print("Проверка провалена")
            return
        
while True:
    main()


