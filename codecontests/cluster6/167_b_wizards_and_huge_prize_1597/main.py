#!/usr/bin/env python3

from collections import defaultdict
from library import FastIO

n, l, a = FastIO.read_ints()
p, s = FastIO.read_ints(), FastIO.read_ints()

m = s.count(-1)

x = {(0, min(a, m)): 1}

r = [1]



for p, s in zip(p, s):

    p /= 100

    if s > 0:

        y = defaultdict(int)

        for (k, a), q in x.items():

            y[(k, a)] += q - q * p

            a = min(m, a + s)

            k = min(l, k + 1)

            y[(k, a)] += q * p

        x = y

    else:

        i = [0] + [q * p for q in r]

        j = [q - q * p for q in r] + [0]

        r = [a + b for a, b in zip(i, j)]



y = [[0] * (m + 1) for i in range(n - m + 1)]

for (k, a), q in x.items():

    if k + a >= l: y[k][a] = q



for k in range(n - m, -1, -1):

    for a in range(m, 0, -1):

        y[k][a - 1] += y[k][a]

for k in range(n - m, 0, -1):

    for a in range(m, -1, -1):

        y[k - 1][a] += y[k][a]



d = 0

for k, p in enumerate(r):

    if l - k <= n - m: d += y[max(0, l - k)][k] * p

print(d)



# Made By Mostafa_Khaled