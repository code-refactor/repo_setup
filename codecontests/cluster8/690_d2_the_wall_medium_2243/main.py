#!/usr/bin/env python3

result=0
mod=10**6 +3
n,C=map(int,input().split()) #recibimos la entrada 
#calc n!
def fact(n):
    fact=1
    for i in range(1,n+1): #1*2*3*...*n = n*(n-1)*(n-2)...*1
        fact=(fact*i)%mod #
    return fact

def pow(a,b): #Algoritmo de Exponenciacion binaria
    exp=1 # Caso base a^1=a
    x=a % mod
    b=b%(mod-1)
    while b > 0: 
        if b % 2 == 1:# En caso que b sea impar
            exp=(exp*x)%mod
            # En caso que b sea impar
        x=(x*x)%mod
        b=b//2
    return exp    

#cacl (n+C)!/(n!*C!) , usamos el pequenno teorema de Fermat a^{p-1}congruente 1(p) a^{p-2}congruente a^{-1}(p)
# de esta forma en vez de 1/n! y 1/C! usamos n!**p-2 C!**p-2 en este caso p=mod 
result=fact(n+C)*pow(fact(n),mod-2)*pow(fact(C),mod-2)-1 # C(n+C,C)= n+C!

print(int(result%mod))