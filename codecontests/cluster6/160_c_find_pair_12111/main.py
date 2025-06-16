#!/usr/bin/env python3

from library import FastIO, MOD
from collections import Counter

INF = 10**9 + 7
MAX = 10**7 + 7

n, k = FastIO.read_ints()
a = FastIO.read_ints()
c = list(Counter(a).items())
c.sort()
#c.append((0, 0))
s = 0
fi = 0
i = 0
while(i<len(c)):
    s += c[i][1]*n
    #print(i, s)
    if(s>=k):
        fi = i
        k -= (s - c[i][1]*n)
        break
    i+=1
si = 0
i = 0
s = 0
while(i<len(c)):
    s += c[i][1]*c[fi][1]
    #print(i, s)
    if(s>=k):
        si = i
        break
    i+=1
print(c[fi][0], c[si][0])
