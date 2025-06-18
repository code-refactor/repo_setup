#!/usr/bin/env python3

from library import read_int, read_str

ALPH = 'abcdefghijklmnopqrstuvwxyz'
MAX = 10 ** 9

def cnt(s):
    c = {ch: 0 for ch in ALPH}
    i = 0
    while i < len(s):
        j = i + 1
        while j < len(s) and s[i] == s[j]:
            j += 1
        c[s[i]] = max(c[s[i]], j - i)
        i = j
    return c

def nxt(c, t):
    nc = cnt(t)
    for ch in ALPH:
        if c[ch] and not nc[ch]:
            nc[ch] = 1
    f = 0
    while f < len(t) and t[f] == t[0]:
        f += 1
    r = 0
    while r < len(t) and t[-1 - r] == t[-1]:
        r += 1
    if t[0] == t[-1]:
        if f == len(t):
            nc[t[0]] = max(nc[t[0]], c[t[0]] + (c[t[0]] + 1) * len(t))
        elif c[t[0]]:
            nc[t[0]] = max(nc[t[0]], f + 1 + r)
    else:
        nc[t[0]] = max(nc[t[0]], f + (c[t[0]] > 0))
        nc[t[-1]] = max(nc[t[-1]], r + (c[t[-1]] > 0))
    return {x: min(MAX, y) for x, y in nc.items()}

n = read_int()
c = cnt(read_str())
for i in range(n - 1):
    c = nxt(c, read_str())
print(max(c.values()))