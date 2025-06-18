#!/usr/bin/env python3

from library import read_ints, DisjointSetUnion, read_test_cases

def solve_test_case():
    """Solve a single test case"""
    n = read_ints()[0]
    p = read_ints()
    
    # Initialize DSU
    dsu = DisjointSetUnion(n)
    
    # Union books that will end up in the same cycle
    for i, target in enumerate(p):
        dsu.union(i, target - 1)  # Convert to 0-indexing
    
    # The number of days it takes for a book to return to its owner
    # is the size of the cycle (connected component) it belongs to
    print(*[dsu.get_size(i) for i in range(n)])

# Process all test cases
read_test_cases(solve_test_case)