#!/usr/bin/env python3

from library import read_ints, count_components, yes_no

def main():
    n, m = read_ints()
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for _ in range(m):
        a, b = read_ints()
        adj[a-1].append(b-1)
        adj[b-1].append(a-1)
    
    # Check if graph is a tree:
    # 1. It must have exactly n-1 edges
    # 2. It must be connected (only one component)
    
    is_tree = (m == n-1) and (count_components(adj) == 1)
    print(yes_no(is_tree, "yes", "no"))

if __name__ == "__main__":
    main()
