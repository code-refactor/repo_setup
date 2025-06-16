#!/usr/bin/env python3

def vasya_and_array():
    n,k,leng = [int(x) for x in input().split()]
    if(leng==1):
        return 0
    a = [int(x) for x in input().split()]
    mod = 998244353
    a.insert(0,0)
    dp = [[0 for x in range((k+1))] for y in range(n+1)]
    sumdp = [0 for _ in range(n+1)]
    sumdp[0]=1
    count = [0 for _ in range(k+1)]
    
    for i in range(1,n+1):
        for j in range(1,k+1):
            if(a[i]==-1 or a[i]==j):
                dp[i][j] = sumdp[i-1]
                count[j]+=1
                if(count[j] >= leng):
                    dp[i][j]-=(sumdp[i-leng] - dp[i-leng][j])
                dp[i][j]%=mod
                sumdp[i]+=dp[i][j]
                sumdp[i]%=mod
            else:
                count[j]=0
        
    return (sumdp[n])
    
print(vasya_and_array()) 