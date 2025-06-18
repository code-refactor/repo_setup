#!/usr/bin/env python3

import sys

input = sys.stdin.readline

def solve():
	n, k = map(int, input().split())
	a = [4,7]
	d = dict()
	idx = 0
	for p in range(1,10):
		for m in range(1<<p):
			v = 0
			for i in range(p):
				v = v*10+a[(m >> i)&1]
			d[v] = idx
			idx += 1
	#print(d)
	c = [0]*idx
	b = 0
	for v in map(int, input().split()):
		if v in d:
			c[d[v]] += 1
		else:
			b += 1
	#print(c,b)
	dp = [[0]*(idx+1) for i in range(idx+1)]
	dp[0][0] = 1
	MOD = int(1e9+7)
	for m in range(1,idx+1):
		dp[m][0] = dp[m-1][0]
		cc = c[m-1]
		for p in range(1,idx+1):
			dp[m][p] = (dp[m-1][p]+dp[m-1][p-1]*cc) % MOD
	res = 0
	d = dp[idx]
	F = [0]*(max(idx,n)+2)
	FI = [0]*(max(idx,n)+2)
	F[0] = 1
	for p in range(1,len(F)):
		F[p] = (F[p-1] * p) % MOD
	FI[-1] = pow(F[-1], MOD-2, MOD)
	for p in range(len(FI)-2,-1,-1):
		FI[p] = (FI[p+1] * (p+1)) % MOD
	#print(d)
	def C(n, k):
		if n < k:
			return 0
		return (F[n]*FI[k]*FI[n-k])%MOD
	for p in range(max(0,k-b),min(idx,k)+1):
		#if b >= k - p:
		#if p >= k - b
		res = (res + d[p]*F[b]*FI[k-p]*FI[b-k+p]) % MOD
	print(res)

solve()
