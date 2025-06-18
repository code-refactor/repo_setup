#!/usr/bin/env python3

from library import read_ints, init_dp_2d, MOD

n, m = read_ints()
A = [0] + sorted(read_ints())

ans = 0
f = init_dp_2d(m + 10, n + 10)

for x in range(1, (A[n] - A[1]) // (m - 1) + 1):
    for i in range(1, n + 1):
        f[1][i] = 1
    
    for i in range(2, m + 1):
        sum_val = 0
        pre = 1
        for j in range(1, n + 1):
            while pre <= n and A[pre] + x <= A[j]:
                sum_val += f[i - 1][pre]
                sum_val %= MOD
                pre += 1
            f[i][j] = sum_val
    
    for i in range(1, n + 1):
        ans += f[m][i]
        ans %= MOD

print(ans)