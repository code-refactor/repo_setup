#!/usr/bin/env python3

from library import fast_power, mod_inverse, MOD

def prob(l_arr, r_arr):
    l_, r_ = max(l_arr), min(r_arr)
   
    if l_ > r_:
        return 1
  
    p = (r_-l_+1)
    for l, r in zip(l_arr, r_arr):
        p *= mod_inverse(r-l+1, MOD)
        
    return (1-p) % MOD

n = int(input())
L = list(map(int, input().split()))
R = list(map(int, input().split()))

EX, EX2 = 0, 0
P = [0] * n
pre = [0] * n

for i in range(1, n):
    P[i] = prob(L[i-1: i+1], R[i-1: i+1])
    pre[i] = (pre[i-1] + P[i]) % MOD
    
    if i >= 2:
        pA, pB, pAB = 1-P[i-1], 1-P[i], 1-prob(L[i-2: i+1], R[i-2: i+1])
        p_ = 1 - (pA+pB-pAB)
        
        EX2 += 2 * (P[i]*pre[i-2] + p_) % MOD

EX = sum(P) % MOD
EX2 += EX
ans = (EX2 + 2*EX + 1) % MOD
print(ans)