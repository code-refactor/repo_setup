#!/usr/bin/env python3

import sys
sys.path.append('/home/justinchiu_cohere_com/minicode/codecontests/cluster5')
from library import read_ints, read_str, create_2d_table

def solve():
    # Read input using library functions
    n, m, k = read_ints()
    s = read_str()
    t = read_str()
    
    # Adjust dimensions (add 1 for DP indexing)
    n_adj = n + 1
    m_adj = m + 1
    
    # Create position array for DP processing
    # Skip positions where (i+1) % n_adj == 0 (boundary positions)
    positions = [i for i in range(n_adj * m_adj - n_adj) if (i + 1) % n_adj]
    reversed_positions = positions[::-1]
    
    # Initialize DP arrays
    # d[i] = length of common suffix ending at position i
    d = [0] * (n_adj * m_adj)
    
    # Fill d array: find common suffixes
    for i in positions:
        row_idx = i % n_adj  # position in string s
        col_idx = i // n_adj  # position in string t
        if s[row_idx] == t[col_idx]:
            d[i] = d[i - n_adj - 1] + 1
    
    # f[i] = maximum total length using i-th position in current configuration
    f = d[:]
    
    # Iterate for k-1 rounds to find k disjoint substrings
    for round_num in range(k - 1):
        # Forward pass: propagate maximum values
        for i in positions:
            f[i] = max(f[i], f[i - 1], f[i - n_adj])
        
        # Backward pass: update with best choices using common suffixes
        for i in reversed_positions:
            # Jump back by the length of common suffix to get non-overlapping substring
            jump_back = d[i] * (n_adj + 1)
            f[i] = f[i - jump_back] + d[i]
    
    # Return maximum value found
    print(max(f))

solve()