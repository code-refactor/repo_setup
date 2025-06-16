#!/usr/bin/env python3

n, a, b, k = map(int, input().split() )
s = input()

mod = (int)( 1e9 + 9 )

ans = 0
t = (int)( (n + 1) / k )

def modInverse(a):
    return pow(a, mod - 2, mod) 

i = 0
for ind in range( len(s) ):
    
    first = ( pow(a, n - i, mod ) * pow( b, i, mod ) ) % mod
    num = ( pow( b, k, mod ) * modInverse( pow(a, k, mod) ) ) % mod
    
    if ( b >= a ) :
        den = ( num - 1 + mod ) % mod
        num = ( pow( num, t, mod ) - 1 + mod ) % mod
    else:
       den = ( 1 - num + mod ) % mod
       num = ( 1 - pow( num, t, mod ) + mod ) % mod
    
    if num == 0:
        temp = ( t * first ) % mod
    else:
        temp = ( num * modInverse(den) ) % mod
        temp = ( temp * first ) % mod
    
    if s[ind] == '+':
        ans = ( ans + temp )%mod
    elif s[ind] == '-':
        ans = ( ans - temp + mod ) % mod
    
    i += 1
    if ( i > n ):
        i = 0

print (ans)