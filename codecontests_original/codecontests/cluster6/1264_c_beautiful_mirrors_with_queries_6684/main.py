#!/usr/bin/env python3

import sys
input = sys.stdin.readline

mod = 998244353 #出力の制限
#互いに素なa,bについて、a*x+b*y=1の一つの解
def extgcd(a,b):
    r = [1,0,a]
    w = [0,1,b]
    while w[2]!=1:
        q = r[2]//w[2]
        r2 = w
        w2 = [r[0]-q*w[0],r[1]-q*w[1],r[2]-q*w[2]]
        r = r2
        w = w2
    #[x,y]
    return [w[0],w[1]]

# aの逆元(mod m)を求める。(aとmは互いに素であることが前提)
def mod_inv(a,m=mod):
    x = extgcd(a,m)[0]
    return (m+x%m)%m

N = int(input())
A = list(map(int, input().split()))

K = 0
P = 0
Q = 1
for i, a in enumerate(A):
    p0 = a * mod_inv(100) % mod
    q0 = (100-a) * mod_inv(100) % mod

    P = (P + (i+1)*Q*q0) % mod
    K = (K + Q*q0) % mod
    Q = Q * p0 % mod

inv = (mod + 1 - K) % mod
w = (N*Q + P) % mod
ans = w * mod_inv(inv) % mod
print(ans)