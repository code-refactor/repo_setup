#!/usr/bin/env python3

def Solve(n,k):
    mod = 10**9+7
    max_n = 10**4
#precalcular los factoriales
    fac = [1] + [0] * max_n
    fac_i = [1] + [0] * max_n
    for i in range(1,n+1):
        fac[i] = fac[i-1] * (i) % mod
        fac_i[i] = fac_i[i- 1] * pow(i,mod-2,mod) % mod

#calculo de las combinaciones con factorial inverso
    def mod_nCr(n,r):
        if n==0 and r==0:
            return 1
        if n<r or n<0:
            return 0
        temp = fac_i[n-r] * fac_i[r] % mod
        return temp * fac[n] % mod

    ans = 0

    for i in range(n + 1): #nos movemos por las filas o columnas seleccionadas
        base = pow(k,n-i,mod) * pow(k-1,i,mod) - pow(k-1,n,mod) + mod  #formas de colocar los numeros en las filas o culmnas 
        base % mod
        val = pow(-1,i) * mod_nCr(n,i) * pow(base,n,mod)    #formas de escoger las i filas o columnas
        ans += val
        ans %= mod
    return ans

    ##el codigo enviado al codeforce aparece debajo de este comentario
n,k = [int(item) for item in input().split()]
mod = 10**9+7
max_n = 10**4

fac = [1] + [0] * max_n
fac_i = [1] + [0] * max_n
for i in range(1,n+1):
    fac[i] = fac[i-1] * (i) % mod
    fac_i[i] = fac_i[i- 1] * pow(i,mod-2,mod) % mod


def mod_nCr(n,r):
    if n==0 and r==0:
        return 1
    if n<r or n<0:
        return 0
    temp = fac_i[n-r] * fac_i[r] % mod
    return temp * fac[n] % mod

ans = 0

for i in range(n + 1):
    base = pow(k,n-i,mod) * pow(k-1,i,mod) - pow(k-1,n,mod) + mod
    base % mod
    val = pow(-1,i) * mod_nCr(n,i) * pow(base,n,mod)
    ans += val
    ans %= mod

print(ans)


