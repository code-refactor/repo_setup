#!/usr/bin/env python3

import sys
reader = (s.rstrip() for s in sys.stdin)
input = reader.__next__

n,m = map(int, input().split())
G = [set() for i in range(n)]
for i in range(m):
    a,b = map(int, input().split())
    a,b = a-1,b-1
    G[a].add(b)
    G[b].add(a)

ans = 0
unused = set(range(n))
while unused:
    cur = {unused.pop()}
    while cur:
        i = cur.pop()
        nxt = {j for j in unused if j not in G[i]}
        unused.difference_update(nxt)
        cur.update(nxt)
    ans += 1
print(ans-1)