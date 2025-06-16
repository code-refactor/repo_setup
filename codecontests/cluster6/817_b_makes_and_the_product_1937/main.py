#!/usr/bin/env python3

from library import Combinatorics

n = int(input())
a = list(map(int, input().split()))
a = sorted(a)
a.append(0)

comb = Combinatorics(n, use_mod=False)
t = 0
while a[3+t] == a[2]:
    t += 1

if a[3] == a[0]:
    ans = comb.C(t+3, 3)
elif a[3] == a[1]:
    ans = comb.C(t+2, 2)
elif a[3] == a[2]:
    ans = t+1
else:
    ans = 1

print(ans)
