#!/usr/bin/env python3

from library import Utils

input = Utils.fast_io()
Utils.set_recursion_limit()

def dfs1(v, parent):
    dp[v] = 1 if colors[v] == 1 else -1
    for u in adj[v]:
        if u != parent:
            dfs1(u, v)
            dp[v] += max(0, dp[u])

def dfs2(v, parent, parent_dp):
    ans[v] = dp[v] + max(0, parent_dp)
    
    child_values = []
    for u in adj[v]:
        if u != parent:
            child_values.append(dp[u])
    
    prefix_sum = [0]
    for val in child_values:
        prefix_sum.append(prefix_sum[-1] + max(0, val))
    
    child_idx = 0
    for u in adj[v]:
        if u != parent:
            # Calculate parent contribution to child u
            # It's current node value + all other children + parent
            other_children = prefix_sum[-1] - max(0, dp[u])
            new_parent_dp = (1 if colors[v] == 1 else -1) + other_children + max(0, parent_dp)
            dfs2(u, v, new_parent_dp)
            child_idx += 1

n = int(input())
colors = [0] + list(map(int, input().split()))
adj = [[] for _ in range(n + 1)]

for _ in range(n - 1):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

dp = [0] * (n + 1)
ans = [0] * (n + 1)

dfs1(1, -1)
dfs2(1, -1, 0)

print(' '.join(map(str, ans[1:])))