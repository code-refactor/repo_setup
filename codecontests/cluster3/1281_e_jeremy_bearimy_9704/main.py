#!/usr/bin/env python3

from library import setup_io, read_int

input = setup_io()

def solve():
    k = read_int()
    n = 2 * k
    e = [[] for i in range(n)]
    p = [None] * n
    
    # Read tree edges
    for i in range(n - 1):
        a, b, t = map(int, input().split())
        a -= 1
        b -= 1
        e[a].append((b, t))
        e[b].append((a, t))
    
    # BFS to create the tree structure
    q = [0]
    qi = 0
    while qi < len(q):
        x = q[qi]
        qi += 1
        px = p[x]
        for v, w in e[x]:
            if v != px:
                q.append(v)
                p[v] = x
    
    # Process from leaves to root
    d1 = [False] * n  # Flag for odd subtrees
    d2 = [0] * n      # Subtree sizes
    m = 0  # Minimum answer
    M = 0  # Maximum answer
    
    for qi in range(len(q) - 1, -1, -1):
        x = q[qi]
        px = p[x]
        cnt = 1   # For parity calculation
        c1 = 1    # For subtree size
        
        for v, w in e[x]:
            if v != px:
                # Handle minimum calculation
                if d1[v]:  # If subtree has odd size
                    m += w
                    cnt += 1
                
                # Handle maximum calculation
                dv = d2[v]
                M += w * min(dv, n - dv)
                c1 += dv
        
        d1[x] = cnt % 2  # Whether this subtree has odd number of nodes
        d2[x] = c1       # Size of this subtree
    
    print(m, M)

# Process multiple test cases
for i in range(read_int()):
    solve()