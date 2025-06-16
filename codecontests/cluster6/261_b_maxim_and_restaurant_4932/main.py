#!/usr/bin/env python3

from library import Combinatorics, FastIO

n = FastIO.read_int()
a = FastIO.read_ints()
p = FastIO.read_int()

comb = Combinatorics(n, use_mod=False)

total = sum(a)
if total <= p:
    print(n)
else:
    ans = 0
    for i in range(n):
        dp = [[[0 for z in range(55)] for y in range(55)] for x in range(55)]
        dp[-1][0][0] = 1
        for j in range(n):
            if j == i:
                for k in range(n):
                    for z in range(p + 1):
                        dp[j][k][z] = dp[j - 1][k][z]
                continue

            for k in range(n):
                for z in range(p + 1):
                    if z + a[j] <= p:
                        dp[j][k + 1][z + a[j]] += dp[j - 1][k][z]
                    dp[j][k][z] += dp[j - 1][k][z]

        for k in range(n):
            for z in range(p + 1):
                if z + a[i] > p:
                    ans += k * dp[n - 1][k][z] * comb.fact[k] * comb.fact[n - k - 1]

    print(ans / comb.fact[n])
