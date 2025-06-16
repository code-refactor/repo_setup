from library import read_array
from collections import *

l = int(input())
c = Counter(read_array(l))
t = defaultdict(int)
p = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]

for k, s in c.items():
    d = 0
    for i, q in enumerate(p):
        while k % q == 0:
            k //= q
            d ^= 1 << i
    t[d] += s

u = defaultdict(int)
u[0] = 1

for x in t:
    if x: l -= 1
    if 0 < x < 2048:
        v = u.copy()
        for y in u: v[x ^ y] += u[y]
        u = v

e = 1000000007
print((u[0] * pow(2, l, e) - 1) % e)