#!/usr/bin/env python3

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def mod_pow(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

n = int(input())
if n == 1:
    print('YES\n1')
    exit(0)
if n == 4:
    print('YES')
    print('1')
    print('3')
    print('2')
    print('4')
    exit(0)
if not is_prime(n):
    print('NO')
    exit(0)
print('YES')
print(1)
for j in range(2, n):
    print(j * mod_pow(j - 1, n - 2, n) % n)
print(n)