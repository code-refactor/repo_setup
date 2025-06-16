#!/usr/bin/env python3

from library import Combinatorics, MOD

comb = Combinatorics()

s = input()
op, cl = 0, s.count(')')
ans = 0
for x in s:
    if x == '(':
        op += 1
        cur = comb.C(cl + op - 1, op)
        ans += cur
    else:
        cl -= 1

print(ans % MOD)
