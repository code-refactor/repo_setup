#!/usr/bin/env python3

from library import read_ints, read_str, create_2d_table

def main():
    n, k = read_ints()
    s = read_str()
    
    # Create DP table using library function
    dp = create_2d_table(n + 1, 26)
    dp[0][0] = 1
    
    for ch in s:
        j = ord(ch) - ord('a')
        for i in range(n, 0, -1):
            dp[i][j] = sum(dp[i - 1])
    
    x = 0
    y = 0
    for i in range(n, -1, -1):
        sum_dp_i = sum(dp[i])
        if x + sum_dp_i >= k:
            print(k * n - y - (k - x) * i)
            break
        x += sum_dp_i
        y += i * sum_dp_i
    else:
        print(-1)

main()
