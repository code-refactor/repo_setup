#!/usr/bin/env python3

from library import setup_io, read_int

input = setup_io()

def solve_test_case():
    n = read_int()
    
    # Read limits for each vertex
    L = []  # Lower limits
    R = []  # Upper limits
    for i in range(n):
        l, r = map(int, input().split())
        L.append(l)
        R.append(r)
    
    # Read tree edges
    adj = [[] for _ in range(n)]
    for i in range(n - 1):
        a, b = map(int, input().split())
        a -= 1  # Convert to 0-indexed
        b -= 1
        adj[a].append(b)
        adj[b].append(a)
    
    # Initialize DP array
    # dp[v][0] = max beauty when vertex v has value L[v]
    # dp[v][1] = max beauty when vertex v has value R[v]
    dp = [[0, 0] for _ in range(n)]
    
    # DFS with stack to avoid recursion limit
    root = 0
    parent = [-1] * n
    
    # First, set up DFS using a stack
    stack = []
    stack.append(~0)  # Post-order marker for root
    stack.append(0)   # Root node
    
    while stack:
        v = stack.pop()
        
        if v >= 0:  # Pre-order processing
            # Add children to stack
            for u in adj[v]:
                if u == parent[v]:
                    continue
                parent[u] = v
                stack.append(~u)  # Post-order marker
                stack.append(u)   # Pre-order
        else:  # Post-order processing
            u = ~v  # Current node (child)
            v = parent[u]  # Parent node
            
            if v == -1:  # Skip root's parent
                continue
                
            # DP transitions:
            # For each child, compute best beauty when parent takes L[v] or R[v]
            
            # If parent takes L[v]:
            # - Child can take L[u]: dp[u][0] + |L[v] - L[u]|
            # - Child can take R[u]: dp[u][1] + |L[v] - R[u]|
            zero = max(dp[u][0] + abs(L[v] - L[u]), dp[u][1] + abs(L[v] - R[u]))
            
            # If parent takes R[v]:
            # - Child can take L[u]: dp[u][0] + |R[v] - L[u]|
            # - Child can take R[u]: dp[u][1] + |R[v] - R[u]|
            one = max(dp[u][0] + abs(R[v] - L[u]), dp[u][1] + abs(R[v] - R[u]))
            
            # Update parent's DP values
            dp[v][0] += zero
            dp[v][1] += one
    
    # Final answer is the maximum beauty when root takes L[0] or R[0]
    return max(dp[0])

def main():
    t = read_int()  # Number of test cases
    for _ in range(t):
        print(solve_test_case())

if __name__ == "__main__":
    main()