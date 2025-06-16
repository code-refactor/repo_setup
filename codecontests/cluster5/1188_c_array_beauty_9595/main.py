#!/usr/bin/env python3

from library import read_ints, create_2d_table, mod_add, MOD2

def main():
    n, m = read_ints()
    A = [0] + sorted(read_ints())

    ans = 0
    
    # Create DP table using library function
    f = create_2d_table(m + 10, n + 10)

    for x in range(1, (A[n] - A[1]) // (m - 1) + 1):
        # Initialize first row
        for i in range(1, n + 1):
            f[1][i] = 1
        
        # Fill DP table
        for i in range(2, m + 1):
            sum_val = 0
            pre = 1
            for j in range(1, n + 1):
                while pre <= n and A[pre] + x <= A[j]:
                    sum_val = mod_add(sum_val, f[i - 1][pre], MOD2)
                    pre += 1
                f[i][j] = sum_val
        
        # Add results for this x
        for i in range(1, n + 1):
            ans = mod_add(ans, f[m][i], MOD2)
    
    print(ans)

main()
