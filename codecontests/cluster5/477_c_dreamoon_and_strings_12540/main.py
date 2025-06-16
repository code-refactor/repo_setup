#!/usr/bin/env python3

import sys
sys.path.append('/home/justinchiu_cohere_com/minicode/codecontests/cluster5')
from library import read_str, create_2d_table

def solve():
    # Read input using library functions
    s = read_str()
    p = read_str()
    
    n = len(s) + 1  # Add 1 for DP indexing
    m = len(p)
    
    # Create 2D DP table using library function
    # dp[i][j] = maximum matches using first i characters with j characters removed
    dp = create_2d_table(n, n, 0)
    
    # For each position in the string
    for pos in range(1, n):
        # Try to match pattern p starting from position pos
        i, j = pos, m
        
        # Match pattern backwards to find if we can complete a match
        while i > 0 and j > 0:
            if s[i - 1] == p[j - 1]:
                j -= 1  # Found matching character
            i -= 1  # Move backwards in string s
        
        # If we matched the entire pattern (j == 0)
        if j == 0:
            # Update DP table: we can form one more match
            pattern_start = i
            pattern_length = m
            
            # For each possible number of characters removed before this match
            for removed_before in range(pattern_start + 1):
                # Characters removed = removed_before + (pos - pattern_start - pattern_length)
                total_removed = removed_before + pos - pattern_start - pattern_length
                if total_removed >= 0:
                    dp[pos][total_removed] = dp[pattern_start][removed_before] + 1
        
        # Carry forward the best results from previous position
        for removed in range(pos):
            dp[pos][removed] = max(dp[pos][removed], dp[pos - 1][removed])
    
    # Output results for removing 0 to n-1 characters
    result = dp[n - 1]
    print(' '.join(map(str, result)))

solve()