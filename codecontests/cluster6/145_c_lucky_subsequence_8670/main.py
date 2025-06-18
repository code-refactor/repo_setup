#!/usr/bin/env python3

from library import read_ints, mod_add, mod_mul, mod_pow, factorial, combination, MOD1

def solve():
    # Read input
    n, k = read_ints()
    sequence = read_ints()
    
    # Lucky digits are 4 and 7
    lucky_digits = [4, 7]
    
    # Generate all lucky numbers and assign unique index to each
    lucky_numbers = {}
    idx = 0
    
    # Generate all lucky numbers up to 10^9 (with up to 9 digits)
    for length in range(1, 10):
        # Try all possible combinations of 4 and 7
        for mask in range(1 << length):
            num = 0
            for i in range(length):
                # Build number by selecting either 4 or 7 based on bit mask
                num = num * 10 + lucky_digits[(mask >> i) & 1]
            lucky_numbers[num] = idx
            idx += 1
    
    # Count occurrences of each lucky number and unlucky numbers
    lucky_counts = [0] * idx
    unlucky_count = 0
    
    for num in sequence:
        if num in lucky_numbers:
            # If it's a lucky number, increment its count
            lucky_counts[lucky_numbers[num]] += 1
        else:
            # Count unlucky numbers separately
            unlucky_count += 1
    
    # Dynamic programming approach
    # dp[m][p] = number of ways to choose p lucky numbers from the first m types
    dp = [[0] * (idx + 1) for _ in range(idx + 1)]
    dp[0][0] = 1  # Base case: 1 way to choose 0 numbers from 0 types
    
    # Fill DP table
    for m in range(1, idx + 1):
        dp[m][0] = dp[m-1][0]  # Ways to choose 0 lucky numbers remains the same
        count = lucky_counts[m-1]  # Count of current lucky number type
        
        for p in range(1, idx + 1):
            # Either don't use current lucky number type, or use it once
            dp[m][p] = (dp[m-1][p] + dp[m-1][p-1] * count) % MOD1
    
    # Calculate result using combinatorics
    result = 0
    d = dp[idx]  # Ways to choose p lucky numbers from all types
    
    # Precompute factorials and their inverses
    max_size = max(idx, n) + 2
    fact = [0] * max_size
    fact_inv = [0] * max_size
    
    # Calculate factorials
    fact[0] = 1
    for i in range(1, max_size):
        fact[i] = (fact[i-1] * i) % MOD1
    
    # Calculate inverse factorials
    fact_inv[-1] = mod_pow(fact[-1], MOD1 - 2, MOD1)
    for i in range(max_size - 2, -1, -1):
        fact_inv[i] = (fact_inv[i+1] * (i+1)) % MOD1
    
    # Calculate final result
    for p in range(max(0, k-unlucky_count), min(idx, k) + 1):
        # Ways to choose p lucky numbers * ways to choose (k-p) unlucky numbers
        term = mod_mul(d[p], mod_mul(fact[unlucky_count], 
                                    mod_mul(fact_inv[k-p], fact_inv[unlucky_count-(k-p)], MOD1), 
                                    MOD1), MOD1)
        result = (result + term) % MOD1
    
    print(result)

if __name__ == "__main__":
    solve()
