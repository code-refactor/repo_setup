#!/usr/bin/env python3

from library import read_ints, DisjointSetUnion

def main():
    n, m = read_ints()
    
    # Create a DSU for each color
    color_graphs = {}
    
    for _ in range(m):
        u, v, c = read_ints()
        if c not in color_graphs:
            color_graphs[c] = DisjointSetUnion(n + 1)  # 1-indexed
        color_graphs[c].union(u, v)
    
    # Process queries
    q = read_ints()[0]
    for _ in range(q):
        u, v = read_ints()
        
        # Count colors that connect u and v
        count = 0
        for c, dsu in color_graphs.items():
            if dsu.is_same_set(u, v):
                count += 1
        
        print(count)

if __name__ == "__main__":
    main()