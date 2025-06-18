#!/usr/bin/env python3

mod=10**9+7
f=[0]*500000

def POW(a,b):
	if(b==0):
		return 1
	if(b&1):
		return POW(a,b//2)**2*a%mod
	else:
		return POW(a,b//2)**2

def C(n,m):
	if(m>n):
		return 0
	t=f[n]*POW(f[m],mod-2)%mod*POW(f[n-m],mod-2)%mod
	return t


f[0]=1
for i in range(1,500000):
	f[i]=f[i-1]*i%mod
a,b,k,t=map(int,input().split(' '))

ans=0
for i in range(0,2*t+1):
	t1=POW(-1,i)*C(2*t,i)%mod
	t2=(C(210000+2*k*t-a+b+2*t-1-(2*k+1)*i+1,2*t)-C(1+2*k*t-a+b+2*t-1-(2*k+1)*i,2*t))%mod
	ans=(ans+t1*t2)%mod
print(ans)
