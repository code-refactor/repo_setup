#!/usr/bin/env python3
from library import read_array, get_bit
from collections import defaultdict

n = int(input())
li = read_array(n)
xori = 0
ans = 0
mul = 1

for i in range(32):
    hashi1 = defaultdict(int)
    hashi0 = defaultdict(int)
    inv1 = 0
    inv2 = 0
    
    for j in li:
        if j // 2 in hashi1 and j % 2 == 0:
            inv1 += hashi1[j // 2]
        if j // 2 in hashi0 and j % 2 == 1:
            inv2 += hashi0[j // 2]
        
        if j % 2:
            hashi1[j // 2] += 1
        else:
            hashi0[j // 2] += 1

    if inv1 <= inv2:
        ans += inv1
    else:
        ans += inv2
        xori = xori + mul
    mul *= 2
    
    for j in range(n):
        li[j] = li[j] // 2

print(ans, xori)