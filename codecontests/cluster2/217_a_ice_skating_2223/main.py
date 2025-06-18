#!/usr/bin/env python3

from library import read_ints, DisjointSetUnion

def main():
    # Read number of snow drifts
    n = read_ints()[0]
    
    # Read coordinates of snow drifts
    drifts = []
    for _ in range(n):
        x, y = read_ints()
        drifts.append((x, y))
    
    # Use DSU to find connected components
    dsu = DisjointSetUnion(n)
    
    # Connect drifts that share an x or y coordinate
    for i in range(n):
        for j in range(i+1, n):
            if drifts[i][0] == drifts[j][0] or drifts[i][1] == drifts[j][1]:
                dsu.union(i, j)
    
    # Count connected components
    component_count = dsu.get_sets_count()
    
    # The answer is the number of components - 1
    # This is because we need n-1 additional drifts to connect n components
    print(component_count - 1)

if __name__ == "__main__":
    main()