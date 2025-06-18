#!/usr/bin/env python3

from library import setup_io, read_int, read_ints, bootstrap
from collections import deque

input = setup_io()

n = read_int()
val = read_ints()
tree = [[] for i in range(n + 1)]
dp = [0 for i in range(n + 1)]
s = [0 for i in range(n + 1)]
ans = [0 for i in range(n + 1)]

# Read tree edges
for i in range(n - 1):
    a, b = map(int, input().split())
    tree[a].append(b)
    tree[b].append(a)

@bootstrap
def dfs1(node, dist, pd):
    for child in tree[node]:
        if child == pd:
            continue
        yield dfs1(child, dist + 1, node)
        dp[node] += dp[child]
        s[node] += s[child]
    dp[node] += val[node - 1] * dist
    s[node] += val[node - 1]
    yield dp[node]

# First pass to compute subtree sums and costs
dfs1(1, 0, 1)

# Second pass to re-root the tree and compute all possible root costs
q = deque()
ans[1] = dp[1]
for node in tree[1]:
    q.append((node, 1))

while len(q) > 0:
    node, pd = q.popleft()
    sub_dp = ans[pd] - (dp[node] + s[node])
    added = s[1] - s[node]
    ans[node] = sub_dp + added + dp[node]
    for child in tree[node]:
        if child == pd:
            continue
        q.append((child, node))

print(max(ans))