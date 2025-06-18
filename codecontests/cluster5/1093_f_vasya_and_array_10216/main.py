#!/usr/bin/env python3

from library import read_ints, init_dp_2d, init_dp_1d

def vasya_and_array():
    n, k, leng = read_ints()
    if leng == 1:
        return 0
    
    a = read_ints()
    mod = 998244353
    a.insert(0, 0)
    
    dp = init_dp_2d(n + 1, k + 1)
    sumdp = init_dp_1d(n + 1)
    sumdp[0] = 1
    count = init_dp_1d(k + 1)
    
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            if a[i] == -1 or a[i] == j:
                dp[i][j] = sumdp[i - 1]
                count[j] += 1
                if count[j] >= leng:
                    dp[i][j] -= (sumdp[i - leng] - dp[i - leng][j])
                dp[i][j] %= mod
                sumdp[i] += dp[i][j]
                sumdp[i] %= mod
            else:
                count[j] = 0
    
    return sumdp[n]

print(vasya_and_array())