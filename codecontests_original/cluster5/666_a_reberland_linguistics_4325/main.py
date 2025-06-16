#!/usr/bin/env python3

from sys import *
setrecursionlimit(200000)
d = {}
t = set()
s = input() + ' '
def gen(l, ll):
    if (l, ll) in t: return
    t.add((l, ll))
    if l > 6:
        d[s[l - 2 : l]] = 1
        if s[l - 2 : l] != s[l : ll]: gen(l - 2, l)
    if l > 7:
        d[s[l - 3 : l]] = 1
        if s[l - 3 : l] != s[l : ll]: gen(l - 3, l)
gen(len(s) - 1,len(s))
print(len(d))
for k in sorted(d): print(k)
 