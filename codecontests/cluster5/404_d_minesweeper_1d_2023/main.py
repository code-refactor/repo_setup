#!/usr/bin/env python3

MOD = 1000000007
s = input()
a, b, c, d = 1, 0, 0, 0

for ch in s:
    if ch == '*':
        a, b, c, d = 0, (a + b + d) % MOD, 0, 0
    elif ch == '?':
        a, b, c, d = (a + b + c) % MOD, (a + b + d) % MOD, 0, 0
    elif ch == '0':
        a, b, c, d = 0, 0, (a + c) % MOD, 0
    elif ch == '1':
        a, b, c, d = 0, 0, b % MOD, (a + c) % MOD
    else:
        a, b, c, d = 0, 0, 0, (b + d) % MOD

print((a + b + c) % MOD)
