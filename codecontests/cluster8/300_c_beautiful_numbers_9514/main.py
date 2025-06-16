#!/usr/bin/env python3

MOD=10**9+7

a,b,n=list(map(int,input().strip().split(' ')))
#there are i a's. n-i b's
def check(a,b,x):
    temp=x%10
    if temp!=a and temp!=b:
        return 0
    while(x>0):
        temp=x%10
        if temp!=a and temp!=b:
            return 0
        x=x//10
    return 1    

fact=[1]
infact=[1]
temp=1
intemp=1
for i in range(1,n+1):
    temp*=i
    #intemp*=pow(i,MOD-2,MOD)
    temp%=MOD
    #intemp%=MOD
    fact+=[temp]
    #infact+=[intemp]
    
def binom(a,b):
    MOD=10**9+7
    if b==0:
        return 1
    else:
        temp=pow(fact[a-b]*fact[b],MOD-2,MOD)*fact[a]
        return temp%MOD
        
        
        
    
    
total=0    
for i in range(n+1):
    temp=i*a+(n-i)*b
    if check(a,b,temp)==1:
        total+=binom(n,i)
        total%=MOD
#total*=fact[a]        
print(total%MOD)      