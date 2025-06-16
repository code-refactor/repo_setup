#!/usr/bin/env python3

# written with help of editorial
n, m = map(int, input().split())
a = list(map(int, input().split()))

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

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

for i in range(1, g + 1):
    if i * i > g:
        break
    if g % i:
        continue
    process(i)
    if i * i != g:
        process(g // i)

print(answer)
