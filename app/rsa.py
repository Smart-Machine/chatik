import random

def gcd(a, b):
    while b != 0:
        a, b = b, a%b
    return a

def generate_primes(n):
    prime = [True for i in range(n + 1)]
    p = 2
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p ** 2, n + 1, p):
                prime[i] = False
        p += 1
    prime[0]= False
    prime[1]= False
    return [p for p in range(n+1) if prime[p]]

def generate_encrypted_key(T: int) -> int:
    for i in range(2, T):
        if gcd(T, i) == 1: 
            return i

def generate_decryption_key(e, T, N: int) -> int:
    for i in range(N):
        if ((e*i) % T) == 1:
            return i

def encrypt_message(msg: str, e, N: int):
    return [(ord(c)**e)%N for c in msg]

def decrypt_message(en_msg, d, N: int):
    plain = [chr((c**d)%N) for c in en_msg]
    return ''.join(plain)
