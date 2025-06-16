#!/usr/bin/env python3

class UnionFindVerSize():
    def __init__(self, N):
        self._parent = [n for n in range(0, N)]
        self._size = [1] * N
        self.group = N

    def find_root(self, x):
        if self._parent[x] == x: return x
        self._parent[x] = self.find_root(self._parent[x])
        stack = [x]
        while self._parent[stack[-1]]!=stack[-1]:
            stack.append(self._parent[stack[-1]])
        for v in stack:
            self._parent[v] = stack[-1]
        return self._parent[x]

    def unite(self, x, y):
        gx = self.find_root(x)
        gy = self.find_root(y)
        if gx == gy: return

        self.group -= 1

        if self._size[gx] < self._size[gy]:
            self._parent[gx] = gy
            self._size[gy] += self._size[gx]
        else:
            self._parent[gy] = gx
            self._size[gx] += self._size[gy]

    def get_size(self, x):
        return self._size[self.find_root(x)]

    def is_same_group(self, x, y):
        return self.find_root(x) == self.find_root(y)

import sys,random,bisect
from collections import deque,defaultdict
from heapq import heapify,heappop,heappush
from itertools import permutations
from math import log,gcd

input = lambda :sys.stdin.buffer.readline()
mi = lambda :map(int,input().split())
li = lambda :list(mi())

def cmb(n, r, mod):
    if ( r<0 or r>n ):
        return 0
    r = min(r, n-r)
    return (g1[n] * g2[r] % mod) * g2[n-r] % mod

mod = 998244353
N = 5100
g1 = [1]*(N+1)
g2 = [1]*(N+1)
inverse = [1]*(N+1)

for i in range( 2, N + 1 ):
    g1[i]=( ( g1[i-1] * i ) % mod )
    inverse[i]=( ( -inverse[mod % i] * (mod//i) ) % mod )
    g2[i]=( (g2[i-1] * inverse[i]) % mod )
inverse[0]=0

n,m,k = mi()

im = pow(m,mod-2,mod)
im_1 = pow(m-1,mod-2,mod)

if n <= k and 1:
    res = 0
    for i in range(n+1):
        res += (cmb(n,i,mod) * pow(im,i,mod) % mod) * (pow(1-im,n-i,mod) * pow(i,k,mod) % mod) % mod
        res %= mod

    print(res)
else:
    dp = [1]
    for i in range(k):
        dp.append(0)
        for j in range(i,-1,-1):
            dp[j+1] += dp[j] * (n-j)
            dp[j+1] %= mod
            dp[j] *= j
            dp[j] %= mod

    if m!=1:
        res = 0
        c = m * im_1 % mod
        for i in range(k+1):
            res += (dp[i] * pow(c,n-i,mod) % mod) * pow(im_1,i,mod) % mod
            res %= mod
        res *= pow((m-1)*im,n,mod)
        res %= mod
        print(res)
    else:
        print(pow(n,k,mod))
