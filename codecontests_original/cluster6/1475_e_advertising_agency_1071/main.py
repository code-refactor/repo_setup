#!/usr/bin/env python3


import math
def c (k, n):
    return (math.factorial(n) // (math.factorial(k) * math.factorial(n - k))) % (10**9 + 7)

def solve():
    n, k = map(int, input().split())
    a = []
    for i in input().split():
        a.append(int(i))
    
    a.sort()
    m = dict()

    for i in a:
        if(m.get(i, 0) == 0): m[i] = 1
        else: m[i] += 1

    ind = n - k
    while ind < n - 1 and a[ind + 1] == a[ind]: ind += 1
    print(c(ind - (n - k) + 1, m[a[n - k]]))

t = int(input())

while t > 0:
    t -= 1
    solve()
