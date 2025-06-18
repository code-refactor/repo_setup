#!/usr/bin/env python3

k, pa, pb = map(int, input().split())

MOD = 10**9 + 7
INF = ((pa + pb) * pow(pb, MOD-2, MOD)) % MOD
rAB = pow(pa+pb, MOD-2, MOD)
rB = pow(pb, MOD-2, MOD)

memo = {}

def dfs(a, ab):
    if ab >= k:
        return ab
    if a + ab >= k:
        #return INF
        #return (pa + pb) / pb
        return ((a + MOD-1) + (pa + pb) * rB + ab) % MOD
        return a - 1 + (pa + pb) / pb + ab
    if (a, ab) in memo:
        return memo[a, ab]
    #res = (((dfs(a+1, ab)+1) * pa * rAB) + ((dfs(a, ab+a)+1) * pb * rAB)) % MOD
    #res = (dfs(a+1, ab)) * pa / (pa + pb) + (dfs(a, ab+a)) * pb / (pa + pb)
    res = (dfs(a+1, ab) * pa * rAB) + (dfs(a, ab+a) * pb * rAB)
    #print(a, ab, res)
    memo[a, ab] = res = res % MOD
    return res
#print((dfs(1, 0) * pa * rAB + 1) % MOD)
#print((pb + dfs(1, 0)*pa) / pa)
print(dfs(1, 0))
