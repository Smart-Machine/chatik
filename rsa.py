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
    # encoded = ""
    # for i in range(len(msg)):
    #     encoded += chr((ord(msg[i])**e)%N)
    # return encoded

    return [(ord(c)**e)%N for c in msg]

def decrypt_message(en_msg, d, N: int):
    # decoded = ""
    # for i in range(len(en_msg)):
    #     decoded += chr((ord(en_msg[i])**d)%N)
    # return decoded

    plain = [chr((c**d)%N) for c in en_msg]
    return ''.join(plain)
    

p = random.choice(generate_primes(1000))
q = random.choice(generate_primes(1000))

# print (p, q)

# N = p*q
# T = (p-1) * (q-1)

# e = generate_encrypted_key(T)
# d = generate_decryption_key(e, T, N)


# msg = "Melissa este in Germania!"


# print (msg)
# enc = encrypt_message(msg, e, N)

# print("Your chipertext is:")
# print(''.join(map(lambda x : str(x), enc)))

# print (enc)
# print(decrypt_message(enc, d, N))
