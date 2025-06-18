#!/usr/bin/env python3

from library import setup_io, read_int

input = setup_io()

def parorder(edge, p):
    """
    Compute parent array and a traversal order using DFS.
    
    Args:
        edge: Adjacency list representation of the tree
        p: Root node
        
    Returns:
        par: Parent array where par[i] is the parent of node i
        order: DFS traversal order
    """
    n = len(edge)
    par = [0] * n
    par[p] = -1
    stack = [p]
    order = []
    visited = set([p])
    ast = stack.append
    apo = order.append
    
    while stack:
        vn = stack.pop()
        apo(vn)
        for vf in edge[vn]:
            if vf in visited:
                continue
            visited.add(vf)
            par[vf] = vn
            ast(vf)
            
    return par, order

def getcld(p):
    """
    Convert parent array to children lists.
    
    Args:
        p: Parent array where p[i] is the parent of node i
        
    Returns:
        res: List of lists where res[i] contains the children of node i
    """
    res = [[] for _ in range(len(p))]
    for i, v in enumerate(p[1:], 1):
        res[v].append(i)
    return res

# Read input
n = read_int()
MOD = 998244353
edge = [[] for _ in range(n)]

# Read edges
for _ in range(n-1):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    edge[a].append(b)
    edge[b].append(a)

# Compute parent-child relationships and traversal order
p, l = parorder(edge, 0)
c = getcld(p)

# DP array:
# dp[i][0]: i is in independent set, its parent is not, i is not marked
# dp[i][1]: i is in independent set, its parent is not, i is marked
# dp[i][2]: i is not in independent set, its parent is in independent set, i is not marked
# dp[i][3]: i is not in independent set, its parent is not in independent set, i is not marked
# dp[i][4]: i is not in independent set, its parent is not in independent set, i is marked
dp = [[1, 1, 0, 0, 1] for _ in range(n)]

# Process nodes in reverse DFS order (bottom-up)
for p in l[::-1]:
    if not c[p]:  # Skip leaf nodes
        continue
        
    res = 1   # Case 0, 1, 4
    res2 = 1  # Case 2
    res3 = 1  # Case 3
    
    for ci in c[p]:
        # For cases 0, 1, 4 (parent not in independent set)
        res = (res * (dp[ci][2] + dp[ci][3] + dp[ci][4])) % MOD
        
        # For case 2 (parent in independent set)
        res2 = (res2 * (dp[ci][1] + dp[ci][2] + 2*dp[ci][3] + dp[ci][4])) % MOD
        
        # For case 3 (parent not in independent set)
        res3 = (res3 * (sum(dp[ci]) + dp[ci][2] + dp[ci][3])) % MOD
    
    dp[p][0] = res
    dp[p][1] = res
    dp[p][2] = (res2 - res) % MOD
    dp[p][3] = (res3 - res) % MOD
    dp[p][4] = res

# Print the answer: all valid ways minus the empty set
print((dp[0][2] + dp[0][3] + dp[0][4] - 1) % MOD)