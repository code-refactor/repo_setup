#!/usr/bin/env python3

mod = 10 ** 9 + 7

def pow_(x, y, p) : 
    res = 1     
    x   = x % p  
      
    if x == 0: 
        return 0
  
    while y > 0: 
        if (y & 1) == 1: 
            res = (res * x) % p 
  
        y = y >> 1 
        x = (x * x) % p 
          
    return res 
    
def reverse(x, mod):
    return pow_(x, mod-2, mod)

def prob(l_arr, r_arr):
    l_, r_ = max(l_arr), min(r_arr)
   
    if l_ > r_:
        return 1
  
    p = (r_-l_+1)
    for l, r in zip(l_arr, r_arr):
        p *= reverse(r-l+1 ,mod)
        
    return (1-p) % mod

n = int(input())
L = list(map(int, input().split()))
R = list(map(int, input().split()))

EX, EX2 = 0, 0
P       = [0] * n
pre     = [0] * n

for i in range(1, n):
    P[i]   =  prob(L[i-1: i+1], R[i-1: i+1])
    pre[i] = (pre[i-1] + P[i]) % mod
    
    if i >= 2:
        pA, pB, pAB = 1-P[i-1], 1-P[i], 1-prob(L[i-2: i+1], R[i-2: i+1])
        p_          = 1 - (pA+pB-pAB)
        
        EX2  += 2 * (P[i]*pre[i-2] + p_) % mod

EX    = sum(P) % mod
EX2  += EX
ans   = (EX2 + 2*EX + 1) % mod
print(ans)