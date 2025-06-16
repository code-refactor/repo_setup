#!/usr/bin/env python3

from itertools import permutations as p

d = lambda a, b: sum((i - j) ** 2 for i, j in zip(a, b))
f = lambda a, b: [i + j - k for i, j, k in zip(a, b, q)]
g = lambda t: sorted(sorted(q) for q in t)

v = [sorted(map(int, input().split())) for i in range(8)]
q = v.pop()

u = g(v)
for a, b, c in p(v, 3):
    for x in p(a):
        s = 2 * d(q, x)
        if not s: continue
        for y in p(b):
            if not 2 * d(q, y) == d(x, y) == s: continue
            for z in p(c):
                if not 2 * d(q, z) == d(x, z) == d(y, z) == s: continue
                t = [x, y, z] + [f(x, y), f(x, z), f(y, z), f(f(x, y), z)]
                if g(t) == u:
                    print('YES')
                    d = [str(sorted(i)) for i in t]
                    for j in v:
                        i = d.index(str(j))
                        k = t.pop(i)
                        print(*k)
                        d.pop(i)
                    print(*q)
                    exit()

print('NO')