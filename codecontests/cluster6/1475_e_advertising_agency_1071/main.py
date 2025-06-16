#!/usr/bin/env python3

from library import Combinatorics

comb = Combinatorics()

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    m = {}
    for i in a:
        m[i] = m.get(i, 0) + 1

    ind = n - k
    while ind < n - 1 and a[ind + 1] == a[ind]: 
        ind += 1
    print(comb.C(m[a[n - k]], ind - (n - k) + 1))

t = int(input())
for _ in range(t):
    solve()
