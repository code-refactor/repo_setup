#!/usr/bin/env python3

from library import MOD2, mod_pow

# Read input
N, M = map(int, input().split())
A = [int(a) for a in input().split()]
B = [int(a) for a in input().split()]

# Calculate total weights of liked and disliked pictures
li = sum([A[i]*B[i] for i in range(N)])
di = sum([(A[i]^1)*B[i] for i in range(N)])

# Initialize with a single state
X = [1]

# Precompute powers for optimization (specific to hard version)
SU = li + di
PO = [0] * (5*M+10)
for i in range(-M-5, 2*M+5):
    PO[i] = pow((SU+i) % MOD2, MOD2-2, MOD2)

# Calculate next distribution
def calc(L):
    su = sum(L)
    pl = 0
    pd = 0
    RE = []
    for i in range(len(L)):
        a = li + i
        b = di - (len(L) - 1 - i)
        pd = b * L[i] * PO[a+b-SU]
        RE.append((pl+pd) % MOD2)
        pl = a * L[i] * PO[a+b-SU]
    RE.append(pl % MOD2)
    return RE

# Calculate all distributions
for i in range(M):
    X = calc(X)

# Calculate expected weights
ne = 0
po = 0
for i in range(M+1):
    po = (po + X[i] * (li + i)) % MOD2
    ne = (ne + X[i] * (di - M + i)) % MOD2

# Calculate inverses
invli = pow(li, MOD2-2, MOD2)
invdi = pow(di, MOD2-2, MOD2)

# Print results
for i in range(N):
    if A[i]:
        print(po * B[i] * invli % MOD2)
    else:
        print(ne * B[i] * invdi % MOD2)
