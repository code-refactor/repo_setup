#!/usr/bin/env python3

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def get_divisors(n):
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(divisors)

# written with help of editorial
n, m = map(int, input().split())
a = list(map(int, input().split()))

g = 0
for x in a:
    g = gcd(g, x - 1)

answer = 0

def process(x):
    global answer
    if x % 2 == 0:
        return 0
    for i in range(30):
        v = 2 ** i * x
        if v > m:
            break
        answer += m - v

divisors = get_divisors(g)
for d in divisors:
    process(d)

print(answer)
