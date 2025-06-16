#!/usr/bin/env python3

import io,os
input=io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
import sys
def solve(n,k):
    mod=998244353
    if k==0:
        ans=1
        for i in range(1,n+1):
            ans*=i
            ans%=mod
        return ans
    if k>=n:
        return 0
    
    inv=lambda x: pow(x,mod-2,mod)
    Fact=[1] #階乗
    for i in range(1,n+1):
        Fact.append(Fact[i-1]*i%mod)
    Finv=[0]*(n+1) #階乗の逆元
    Finv[-1]=inv(Fact[-1])
    for i in range(n-1,-1,-1):
        Finv[i]=Finv[i+1]*(i+1)%mod
    def comb(n,r):
        if n<r:
            return 0
        return Fact[n]*Finv[r]*Finv[n-r]%mod
    
    m=n-k
    t=1
    ans=0
    for r in range(m,0,-1):
        ans+=t*comb(m,r)*pow(r,n,mod)
        ans%=mod
        t*=-1
    ans*=comb(n,m)*2
    ans%=mod
    return ans

def main():
    n,k=map(int,input().split())
    ans=solve(n,k)
    sys.stdout.write(str(ans)+'\n')
    
if __name__=='__main__':
    main()