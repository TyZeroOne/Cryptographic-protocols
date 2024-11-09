import random
import math
import hashlib

def is_prime(n, k=100):
    if n <= 1:
        return False
    if n == 2:
        return True
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True

def length(a):
    b = pow(10, a - 1)
    c = pow(10, (a)) - 1
    return b, c

def hash_file(filename):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash.update(byte_block)
    return hash.hexdigest()

def generate_prime(limit):
    a, b = length(limit)
    prime_candidate = random.randint(a, b)
    while not is_prime(prime_candidate):
        prime_candidate = random.randint(a, b)
    return prime_candidate

def generate_keys(number):
    p = generate_prime(number)
    q = generate_prime(number)
    while (p == q):
        p = generate_prime(number)
        q = generate_prime(number)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = random.randint(2, phi_n - 1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)
    s = pow(e, -1, phi_n)
    J = int(hash_file('Alice.txt'), 16)
    J_s = pow(int(J), s, n)
    x = pow(J_s, -1, n)
    y = pow(x, e, n)
    public_key = (n, e, y)
    private_key = (x,)
    return public_key, private_key

def message_signature(public, private, M):
    n, e, y = public
    x = private[0]
    e, n, x = int(e), int(n), int(x)
    r = random.randint(1, n - 1)
    a = pow(r, e, n)
    new_message = f"{M}{a}"
    d = hashlib.md5()
    d.update(new_message.encode('utf-8'))
    d = int(d.hexdigest(), 16) % e
    z = r * pow(x, d, n) % n
    J = int(hash_file('Alice.txt'), 16)
    return (d, z, J)

def write_to_file(files, message):
    with open(files, 'w') as file:
        file.write(','.join(map(str, message)))

def open_file(files):
    with open(files, 'r') as file:
        data = tuple(map(str, file.read().split(',')))
    return data

def signature_verification(sign, M, public):
    n, e, y = public
    e, n = int(e), int(n)
    d, z, J = sign
    d, z, J = int(d), int(z), int(J)
    a_ = pow(z, e, n) * pow(J, d, n) % n
    d_ = hashlib.md5()
    new_message = f'{M}{a_}'
    d_.update(new_message.encode('utf-8'))
    d_ = int(d_.hexdigest(), 16) % e
    if d_ == d:
        print('Подпись действительна')
    else:
        print('Подпись недействительна')
    return

def main():
    print("Введите 1 для генерации ключей")
    print("Введите 2 для подписи документа")
    print("Введите 3 для проверки подписи")
    a = input("Введите режим работы: ")
    if a == "1":
        i = input("Введите количество символов в числе: ")
        public_key, private_key = generate_keys(int(i))
        write_to_file('public_key.txt', public_key)
        write_to_file('private_key.txt', private_key)
        print(f"Публичный ключ: {public_key}\nПриватный ключ: {int(private_key[0])}")
    elif a == "2":
        try:
            with open('input.txt', 'r', encoding='utf-8') as file:
                plaintext = file.read()
            public_key = open_file('public_key.txt')
            private_key = open_file('private_key.txt')
            if len(public_key) == 0 or len(private_key) == 0 or len(plaintext) == 0:
                print("Error reading")
                return
            sign = message_signature(public_key, private_key, plaintext)
            with open('signature.txt', 'w', encoding='utf-8') as file:
                file.write(str(sign))
            print(f"Подпись состоит из следующего: \nЗначения d: {sign[0]}\
                \nЗначения z: {sign[1]}\nАтрибутов J: {sign[2]}")
        except Exception as e:
            print("Error: ", e)
    elif a == "3":
        try:
            with open('input.txt', 'r', encoding='utf-8') as file:
                plaintext = file.read()
            public_key = open_file('public_key.txt')
            with open('signature.txt', 'r', encoding='utf-8') as file:
                sign = eval(file.read())
            if len(sign) == 0 or len(public_key) == 0:
                print("Error reading")
                return
            signature_verification(sign, plaintext, public_key)
        except Exception as e:
            print("Error: ", e)
    else:
        print("Неверный выбор")
while True:
    main()
