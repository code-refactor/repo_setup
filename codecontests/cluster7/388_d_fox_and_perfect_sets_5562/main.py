#!/usr/bin/env python3

from library import read_int

def solve():
    """
    Solve the Fox and Perfect Sets problem.
    
    A Perfect Set has the property that the XOR of all non-empty subsets equals k.
    We need to count such sets modulo 10^9+7.
    
    The solution uses dynamic programming to build sets bit by bit.
    """
    MOD = 10**9 + 7
    
    # Read input
    k = read_int()
    
    # Convert k to binary representation (without '0b' prefix)
    binary_k = list(map(int, bin(k)[2:]))
    N = len(binary_k)
    
    # Initialize DP array
    # dp[i][j][b] = number of ways to construct a set using i bits, j bases,
    # where b=1 if current XOR matches the corresponding prefix of k, b=0 otherwise
    dp = [[[0, 0] for j in range(i + 2)] for i in range(N + 1)]
    
    # Base case: empty set with empty prefix matches
    dp[0][0][1] = 1
    
    # Fill the DP table
    for i in range(1, N + 1):
        for j in range(i + 1):
            # Case 1: Current XOR doesn't match prefix of k
            
            # 1a: If previous XOR didn't match, it still won't match
            # When distributing elements to subsets (2^j ways) or adding a new base
            dp[i][j][0] += 2**j * dp[i-1][j][0]  # Distribute elements
            if j > 0:
                dp[i][j][0] += dp[i-1][j-1][0]  # Add new base element
            
            # 1b: Previous XOR matched but current bit makes it mismatch
            odd_subsets = 2**(j-1) if j else 0
            even_subsets = 2**j - odd_subsets
            
            if binary_k[i-1] == 1:
                # If k's bit is 1, distributing to even subsets causes mismatch
                dp[i][j][0] += even_subsets * dp[i-1][j][1]
            
            # Case 2: Current XOR matches prefix of k
            
            if binary_k[i-1] == 0:
                # If k's bit is 0, distributing to even subsets maintains match
                dp[i][j][1] += even_subsets * dp[i-1][j][1]
            else:
                # If k's bit is 1, distributing to odd subsets maintains match
                dp[i][j][1] += odd_subsets * dp[i-1][j][1]
                
                # Adding a new base element flips one bit (adds to odd count)
                if j > 0:
                    dp[i][j][1] += dp[i-1][j-1][1]
    
    # Sum all possible configurations
    total = sum(sum(row) for row in dp[-1])
    
    return total % MOD

if __name__ == '__main__':
    print(solve())