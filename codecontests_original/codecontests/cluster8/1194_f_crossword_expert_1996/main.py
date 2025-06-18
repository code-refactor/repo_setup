#!/usr/bin/env python3

mod = 10 ** 9 + 7
MAX = 2 * 10 ** 5+2
 
r = [1] * MAX  
factorial = [1] * MAX
rfactorial = [1] * MAX
rp = [1] * MAX 

#Permite precalcular factorial hasta "MAX", para evitar tener que calcularlo varias veces
#dentro de la ejecucion del programa.
for i in range(2, MAX):
    factorial[i]   = i * factorial[i - 1] % mod
    
    r[i] = mod - (mod // i) * r[mod%i] % mod

    rfactorial[i] = rfactorial[i-1] * r[i] % mod

#Calcula el inverso de "p" para evitar usar fracciones racionales.    
for i in range(1, MAX):
    rp[i] = rp[i - 1] * (mod + 1) // 2 % mod
    
n, T = list(map(int, input().split()))
t = list(map(int, input().split()))
t.append(10**10+1)

#Permite calcular las Combinacione de n en k.
def Combination(n,k):
    return factorial[n]*rfactorial[k]*rfactorial[n-k]
 
S=0
E=0

for i in range(0,n+1):
    sim = 0
    for add in range(2):
        l_, r_ =  max(0, T-S-t[i] + add), min(i, T-S)
        
        for x in range(l_, r_+1):
            sim += Combination(i,x) * rp[i+1]    
    E = (E + i * sim) % mod
    S += t[i]   
    
print(E)
