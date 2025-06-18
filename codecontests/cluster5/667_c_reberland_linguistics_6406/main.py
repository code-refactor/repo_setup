#!/usr/bin/env python3

from library import read_str, init_dp_1d

s = read_str()[5:][::-1]
n = len(s)

mu = set()
can2 = init_dp_1d(n + 1, 0)
can3 = init_dp_1d(n + 1, 0)

if n >= 2:
    mu.add(s[0:2][::-1])
    can2[2] = 1
if n >= 3:
    mu.add(s[0:3][::-1])
    can3[3] = 1
if n >= 4 and s[0:2] != s[2:4]:
    mu.add(s[2:4][::-1])
    can2[4] = 1
if n >= 5:
    mu.add(s[2:5][::-1])
    mu.add(s[3:5][::-1])
    can2[5] = 1
    can3[5] = 1
        
for i in range(6, n + 1):
    if can2[i - 3]:
        mu.add(s[i - 3:i][::-1])
        can3[i] = 1
    if can2[i - 2]:
        if s[i - 2:i] != s[i - 4:i - 2]:
            mu.add(s[i - 2:i][::-1])
            can2[i] = 1  
    if can3[i - 2]:
        mu.add(s[i - 2:i][::-1])
        can2[i] = 1
    if can3[i - 3]:
        if s[i - 3:i] != s[i - 6:i - 3]:
            mu.add(s[i - 3:i][::-1])
            can3[i] = 1

print(len(mu))
print('\n'.join(sorted(list(mu))))