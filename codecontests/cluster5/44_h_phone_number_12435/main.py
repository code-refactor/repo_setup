#!/usr/bin/env python3

from library import read_str, create_2d_table

def main():
    a = read_str()
    n = len(a)
    
    # Create DP table using library function
    dp = create_2d_table(n, 10)
    
    # Initialize first row
    for i in range(10):
        dp[0][i] = 1
    
    # Fill DP table
    for i in range(n - 1):
        for j in range(10):
            if dp[i][j] != 0:
                c = (int(a[i + 1]) + j) // 2
                d = (int(a[i + 1]) + j + 1) // 2
                if c != d:
                    dp[i + 1][c] += dp[i][j]
                    dp[i + 1][d] += dp[i][j]
                else:
                    dp[i + 1][c] += dp[i][j]
    
    # Calculate total possibilities
    s = sum(dp[-1])
    
    # Check if original string is valid
    t = 0
    c = int(a[0])
    f = [a[0]]
    for i in range(1, n):
        d = (c + int(a[i])) // 2
        e = (c + int(a[i]) + 1) // 2
        if int(a[i]) == d:
            f.append(a[i])
            c = d
        elif int(a[i]) == e:
            f.append(a[i])
            c = e
        else:
            break
    
    if "".join(f) == a:
        t = 1
    
    print(s - t)

main()