#!/usr/bin/env python3

import math

n = int(input())
a = [int(x) for x in input().split()]
p = int(input())

sum=0;
for x in range(n):
	sum+=a[x]
if(sum<=p):
	print(n)
else:
	ans=0
	for i in range(n):
		dp = [[[0 for z in range(55)] for y in range(55)] for x in range(55)]
		dp[-1][0][0]=1
		for j in range(n):
			if(j==i):

				for k in range(n):
					for z in range(p+1):
						dp[j][k][z]=dp[j-1][k][z]
				continue

			for k in range(n):

				for z in range(p+1):

					if(z+a[j]<=p):
						dp[j][k+1][z+a[j]]+=dp[j-1][k][z]
					dp[j][k][z]+=dp[j-1][k][z]


		for k in range(n):
			for z in range(p+1):
				if(z+a[i]>p):
					ans+=k*dp[n-1][k][z]*math.factorial(k)*math.factorial(n-k-1)

	print(ans/math.factorial(n))
