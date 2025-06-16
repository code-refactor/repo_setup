#!/usr/bin/env python3

from library import read_ints, create_3d_table, mod_add

MOD = 100000000

def main():
    n1, n2, k1, k2 = read_ints()
    k1 = min(k1, n1)
    k2 = min(k2, n2)
    
    # Create 3D DP table using library function
    dp = create_3d_table(n1 + 1, n2 + 1, 2)
    
    # Initialize base cases
    for i in range(k1 + 1):
        dp[i][0][0] = 1
    for i in range(k2 + 1):
        dp[0][i][1] = 1
    
    # Fill DP table
    for i in range(1, n1 + 1):
        for j in range(1, n2 + 1):
            # Sum transitions for footman (type 0)
            dp[i][j][0] = sum(dp[k][j][1] for k in range(max(0, i - k1), i)) % MOD
            # Sum transitions for horseman (type 1)  
            dp[i][j][1] = sum(dp[i][k][0] for k in range(max(0, j - k2), j)) % MOD
    
    result = mod_add(dp[n1][n2][0], dp[n1][n2][1], MOD)
    print(result)

main()