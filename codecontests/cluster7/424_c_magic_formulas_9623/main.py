#!/usr/bin/env python3

import sys
input=sys.stdin.readline
n=int(input())
ar=list(map(int,input().split()))
dp=[0]
pre=0
for i in range(1,n+1):
    pre^=i
    dp.append(pre)
ans=0
for i in range(1,n+1):
    xx=ar[i-1]^(dp[i-1]*((n//i)%2))^(dp[n%i])
    ans^=xx
print(ans)