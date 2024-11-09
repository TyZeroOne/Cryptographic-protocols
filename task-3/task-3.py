import random
import hashlib 
import sympy

def mod_inverse(a, q):
    return pow(a, -1, q)

def gen_param(bits):
    q = random.getrandbits(bits)
    while not sympy.isprime(q):
        q = random.getrandbits(bits)
    i = 2
    while True:
        p = q * i + 1
        if sympy.isprime(p):
            break
        i += 1
    g = 1
    while g == 1:
        h = random.randint(2, p - 1)
        g = pow(h, (p - 1) // q, p)  
    return p, q, g
        
def generate_keys(p, q, g):
    private = random.randint(1, q - 1)
    public = pow(g, private, p) 
    return private, public

def sign_message(p, q, g, x, message):
    k = random.randint(1, q - 1)
    r = pow(g, k, p) % q
    while r == 0:
        k = random.randint(1, q - 1)
        r = pow(g, k, p) % q
    k_inv = mod_inverse(k, q)
    hash_m = hashlib.sha1()
    hash_m.update(message.encode('utf-8'))
    hash_m = int(hash_m.hexdigest(), 16)
    s = (k_inv * (hash_m + x * r)) % q
    if s == 0:
        return sign_message(p, q, g, x, message)  
    return r, s

def verify_signature(p, q, g, y, message, r, s):
    if not (0 < r < q and 0 < s < q):
        return False
    hash_m = hashlib.sha1()
    hash_m.update(message.encode('utf-8'))
    hash_m = int(hash_m.hexdigest(), 16)
    w = mod_inverse(s, q)
    u1 = (hash_m * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    return v == r

def write_to_file(files, message):
    with open(files, 'w') as file:
        file.write(','.join(map(str, message)))

def open_file(files):
    with open(files, 'r') as file:
        data = tuple(map(str, file.read().split(',')))
    return data

def main():
    print("Введите 1 для генерации ключей")
    print("Введите 2 для подписи документа")
    print("Введите 3 для проверки подписи")
    k = int(input("Введите режим работы: "))
    try:
        if k == 1:
            with open('input.txt', 'r', encoding='utf-8') as file:
                message = file.read()
            hash_m = hashlib.sha1()
            hash_m.update(message.encode('utf-8'))
            hash_m = int(hash_m.hexdigest(), 16)
            tmp = bin(hash_m)
            p, q, g = gen_param(len(tmp) - 2)
            print("Параметр p: ", p)
            print("Параметр q: ", q)
            print("Параметр g: ", g)
            write_to_file("parametrs.txt", (p, q, g))
            private, public = generate_keys(p, q, g)
            print("Приватный ключ: ", private)
            print("Публичный ключ: ", public)
            with open("private_key.txt", 'w') as file:
                file.write(str(private))
            with open("public_key.txt", 'w') as file:
                file.write(str(public))
        elif k == 2:
            p, q, g = open_file("parametrs.txt")
            private = open_file("private_key.txt")[0]
            with open('input.txt', 'r', encoding='utf-8') as file:
                message = file.read()
            r, s = sign_message(int(p), int(q), int(g), int(private), message)
            print("Параметр r: ", r)
            print("Параметр s: ", s)
            write_to_file("signed_message.txt", (r, s))
        elif k == 3:
            p, q, g = open_file("parametrs.txt")
            public = open_file("public_key.txt")[0]
            r, s = open_file("signed_message.txt")
            with open('input.txt', 'r', encoding='utf-8') as file:
                message = file.read()
            if verify_signature(int(p), int(q), int(g), int(public), message, int(r), int(s)):
                print("Подпись действительна")
                return
            else:
                print("Подпись недействительна")
                return
    except Exception as e:
        print("Error: ", e)
while True:
    main()