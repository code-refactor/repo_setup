#!/usr/bin/env python3

from library import MOD2, mod_inverse

P = MOD2
N, M = map(int, input().split())
A = [int(a) for a in input().split()]
B = [int(a) for a in input().split()]
li = sum([A[i]*B[i] for i in range(N)])
di = sum([(A[i]^1)*B[i] for i in range(N)])
X = [1]
SU = li+di
PO = [0] * (5*M+10)
for i in range(-M-5, 2*M+5):
    PO[i] = mod_inverse((SU+i)%P, P)

def calc(L):
    su = sum(L)
    pl = 0
    pd = 0
    RE = []
    for i in range(len(L)):
        a = li + i
        b = di - (len(L) - 1 - i)
        pd = b * L[i] * PO[a+b-SU]
        RE.append((pl+pd)%P)
        pl = a * L[i] * PO[a+b-SU]
    RE.append(pl%P)
    return RE

for i in range(M):
    X = calc(X)
ne = 0
po = 0
for i in range(M+1):
    po = (po + X[i] * (li + i)) % P
    ne = (ne + X[i] * (di - M + i)) % P
invli = mod_inverse(li, P)
invdi = mod_inverse(di, P)
for i in range(N):
    print(po * B[i] * invli % P if A[i] else ne * B[i] * invdi % P)
