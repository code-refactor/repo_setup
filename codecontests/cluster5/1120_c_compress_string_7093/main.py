#!/usr/bin/env python3

from library import z_function

a=list(map(int,input('').split()))
n,a,b=a[0],a[1],a[2]
s=input('')
dp=[0 for i in range(n)]
dp[0]=a
for i in range(1,n):
    t=s[:i+1]
    dp[i]=dp[i-1]+a
    q=z_function(t[::-1])
    maxs=[0 for j in range(i+1)]
    maxs[0]=q[i]
    for j in range(1,i):
        maxs[j]=max(maxs[j-1],q[i-j])
    for j in range(i):
        if maxs[j]>=i-j:
            dp[i]=min(dp[i],dp[j]+b)
print(dp[len(dp)-1])
            
