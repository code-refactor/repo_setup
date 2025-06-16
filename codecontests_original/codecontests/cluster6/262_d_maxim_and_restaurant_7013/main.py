#!/usr/bin/env python3

n=int(input())
arr=list(map(int,input().split()))
p=int(input())
dp=[[[0 for k in range(n+1)] for i in range(p+1)] for i in range(n+1)]
for j in range(p+1):
    for k in range(n+1):
        dp[0][j][k]=1
for i in range(1,n+1):
    for j in range(p+1):
        for k in range(1,n+1):
            if j>=arr[k-1]:
                dp[i][j][k]=dp[i][j][k-1]+i*dp[i-1][j-arr[k-1]][k-1]
            else:
                dp[i][j][k]=dp[i][j][k-1]
fact=n
ans=0
for i in range(1,n+1):
    ans+=dp[i][p][n]/fact
    fact*=(n-i)
print(ans)
