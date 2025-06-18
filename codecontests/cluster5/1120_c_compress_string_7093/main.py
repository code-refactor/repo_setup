#!/usr/bin/env python3

def f(x):
    z=[0 for i in range(len(x))]
    l=0
    r=0
    for i in range(1,len(x)):
        if i<=r:
            z[i]=min(z[i-l],r-i+1)
        while i+z[i]<len(x) and x[z[i]]==x[i+z[i]]:
            z[i]+=1
        if i+z[i]-1>r:
            l,r=i,i+z[i]-1
    return z
a=list(map(int,input('').split()))
n,a,b=a[0],a[1],a[2]
s=input('')
dp=[0 for i in range(n)]
dp[0]=a
for i in range(1,n):
    t=s[:i+1]
    dp[i]=dp[i-1]+a
    q=f(t[::-1])
    maxs=[0 for j in range(i+1)]
    maxs[0]=q[i]
    for j in range(1,i):
        maxs[j]=max(maxs[j-1],q[i-j])
    for j in range(i):
        if maxs[j]>=i-j:
            dp[i]=min(dp[i],dp[j]+b)
print(dp[len(dp)-1])
            
