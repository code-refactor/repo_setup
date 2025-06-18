#!/usr/bin/env python3

from library import MOD2, mod_pow

# Read input
N, M = map(int, input().split())
A = [int(a) for a in input().split()]
B = [int(a) for a in input().split()]

# Calculate total weights of liked and disliked pictures
li = sum([A[i]*B[i] for i in range(N)])
di = sum([(A[i]^1)*B[i] for i in range(N)])

# Initialize DP table
X = [[] for _ in range(M+1)]
X[0] = [1]

# Calculate next distribution
def calc(L):
    su = sum(L)
    pl = 0
    pd = 0
    RE = []
    for i in range(len(L)):
        a = li + i
        b = di - (len(L) - 1 - i)
        pd = b * L[i] * pow(su*(a+b), MOD2-2, MOD2)
        RE.append((pl+pd)%MOD2)
        pl = a * L[i] * pow(su*(a+b), MOD2-2, MOD2)
    RE.append(pl%MOD2)
    return RE

# Calculate all distributions
for i in range(M):
    X[i+1] = calc(X[i])

# Calculate expected weights
ne = 0
po = 0
for i in range(M+1):
    po = (po + X[M][i] * (li + i)) % MOD2
    ne = (ne + X[M][i] * (di - M + i)) % MOD2

# Print results
for i in range(N):
    if A[i]:
        print(po * B[i] * pow(li, MOD2-2, MOD2) % MOD2)
    else:
        print(ne * B[i] * pow(di, MOD2-2, MOD2) % MOD2)
