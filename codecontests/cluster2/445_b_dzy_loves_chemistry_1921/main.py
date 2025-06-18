#!/usr/bin/env python3

from library import read_ints, DisjointSetUnion

def main():
    # Read input
    n, m = read_ints()
    
    # Initialize DSU
    dsu = DisjointSetUnion(n)
    
    # Process each reaction pair
    for _ in range(m):
        a, b = read_ints()
        # Convert to 0-indexed
        dsu.union(a-1, b-1)
    
    # Count number of connected components
    components = dsu.get_sets_count()
    
    # Calculate maximum danger
    # For each component, we can multiply the danger by 2^(size-1)
    # Total danger is 2^(n-components)
    max_danger = 2**(n-components)
    
    print(max_danger)

if __name__ == "__main__":
    main()
