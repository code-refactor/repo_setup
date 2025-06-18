#!/usr/bin/env python3

from library import read_int
from fractions import Fraction

# Read input
n = read_int()

# Initialize tree and DP arrays
adj = [[] for _ in range(n)]
H = [0] * n  # Max product when subtree rooted at node i is a connected component
F = [0] * n  # Product of child H values
FoH = [[] for _ in range(n)]  # Ratio of F/H for each child, used for optimization

# Arrays for DFS traversal
sz = 0
order = [0] * n  # Post-order traversal
parent = [-1] * n  # Parent array

def dfs(node, p=-1):
    """DFS to set up parent pointers and post-order traversal."""
    global sz
    parent[node] = p
    
    for neighbor in adj[node]:
        if neighbor != p:
            dfs(neighbor, node)
    
    order[sz] = node
    sz += 1

def solve(node, p=-1):
    """Calculate optimal solution for subtree rooted at node."""
    global H, F, FoH
    
    # Base value: just this node
    F[node] = 1
    
    # Calculate F[node] = product of all H[child] values
    for child in adj[node]:
        if child != p:
            F[node] *= H[child]
            FoH[node].append(Fraction(F[child], H[child]))
    
    # Initial answer is just the product of subtrees
    ans = F[node]
    
    # Sort child ratios for greedy selection
    FoH[node].sort(reverse=True)
    
    # Try cutting some children off from this node
    product = 1
    count = 0
    for ratio in FoH[node]:
        product *= ratio
        count += 1
        # New answer: (product of selected children's F) * (original F / product of their H) * (count + 1)
        # where count + 1 includes this node
        ans = max(ans, int(product * F[node]) * (count + 1))
    
    # Try treating this node and some of its children as a special case
    for child in adj[node]:
        if child != p:
            product = 1
            count = 0
            for ratio in FoH[child]:
                product *= ratio
                count += 1
                # Special case: this node + some of child's children form a component
                component_value = int(product * F[node] * F[child]) // H[child] * (count + 2)
                ans = max(ans, component_value)
    
    # Set H[node] to the optimal value
    H[node] = ans

# Read tree edges
for i in range(1, n):
    u, v = map(int, input().split())
    u -= 1  # Convert to 0-indexed
    v -= 1
    adj[u].append(v)
    adj[v].append(u)

# Run DFS to get order and parent pointers
dfs(0)

# Process nodes in post-order to compute optimal values
for node in order:
    solve(node, parent[node])

# Print the maximum product
print(H[0])