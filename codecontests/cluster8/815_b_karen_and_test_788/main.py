#!/usr/bin/env python3

from sys import exit, stdin, stdout
n = int(stdin.readline())
a = [int(i) for i in stdin.readline().split()]
if n == 1:
    print(a[0])
    exit(0)
mod = 1000000007
f = [0] * (n + 1)
f[0] = 1
for i in range(1, n + 1):
    f[i] = (f[i-1] * i) % mod

def f_pow(a, k):
    if k == 0:
        return 1
    if k % 2 == 1:
        return f_pow(a, k - 1) * a % mod
    else:
        return f_pow(a * a % mod, k // 2) % mod

def c(n, k):
    d = f[k] * f[n - k] % mod
    return f[n] * f_pow(d, mod - 2) % mod
     
oper = 1
while not (oper and n % 2 == 0):
    for i in range(n - 1):
        a[i] = a[i] + oper * a[i + 1]
        oper *= -1
    n -= 1
oper *= 1 if (n//2 % 2) != 0 else -1

sm1 = 0
sm2 = 0
for i in range(n):
    if i % 2 == 0:
        sm1 = (sm1 + c(n // 2 - 1, i // 2) * a[i]) % mod
    else:
        sm2 = (sm2 + c(n // 2 - 1, i // 2) * a[i]) % mod
stdout.write(str((sm1 + oper * sm2) % mod))
