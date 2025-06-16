#!/usr/bin/env python3

from library import FastIO

def num_ones(a,b):
    '''returns how many nums start
    with digit 1 in [a,b]'''
    if a==0:
        if b==0:
            return 0
        ans=0
        b=str(b)
        for i in range(1,len(b)):
            ans+=10**(i-1)
        if b[0]=='1':
            x=b[1:]
            if x=='':
                x=0
            else:
                x=int(x)
            ans+=x+1
        else:
            ans+=10**(len(b)-1)
        return ans
    return num_ones(0,b)-num_ones(0,a-1)
        
        
def dp(far,need):
    '''returns prob that the first
    far vars have at least need 1s'''

    if DP[far][need]!=-1:
        return DP[far][need]
    if need>(far+1):
        return 0
    if need==0:
        return 1
    if far==0:
        return L[0]
    ans=L[far]*dp(far-1,need-1)+(1-L[far])*dp(far-1,need)
    DP[far][need]=ans
    return ans

n = FastIO.read_int()
L = []
for i in range(n):
    s = FastIO.read_ints()
    L.append(num_ones(s[0], s[1]) / (s[1] - s[0] + 1))
k = FastIO.read_int()
atLeast=int((n*k-1)/100)+1
if k==0:
    atLeast=0
DP=[]
for i in range(n):
    DP.append([-1]*(atLeast+5))

print(round(dp(n-1,atLeast),10))


