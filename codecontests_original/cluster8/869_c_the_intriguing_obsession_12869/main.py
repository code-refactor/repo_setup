#!/usr/bin/env python3

a,b,c = list(map(int, input().split(' ')))


MOD = 998244353

def d(a, b):
	s = 1
	for i in range(a, b+1):
		s*=i
		s%=MOD
	return s




def cnk(n,k):
	s = 1
	for i in range(n-k+1, n+1):
		s*=i
	for i in range(1,k+1):
		s/=i
	return s


def factorial(n):
	s = 1
	for i in range(1, n+1):
		s*=i	
	return s



def pow(a, b):
	c = 1

	while b>0:
		if b%2==0:
			b//=2
			a *=a
			a%=MOD
		else:
			b-=1
			c*=a
			c%=MOD
	return c


def inv(i):
	return pow(i, MOD-2)
"""
def factinv(i):

	return 1.0/factorial(i)

"""
fi = [1, 1]
def sp(n, m):
	s = 1
	d1 = 1
	d2 = 1
	#print(d1,d2,"!")
	for i in range(1, n+1):
		d1*=n-i+1
		d2*=m-i+1

		#print(i, d1,d2)
		d1%=MOD
		d2%=MOD
		s+= d1*d2 *(fi[i]%MOD)
		#print(d1*d2 *(fi[i]%MOD))
		s%= MOD

	return s



s = 1
for i in range(2, max(a,max(b,c))+1):
	s *=i
	s %= MOD
	fi.append(inv(s))


print((sp(a,b)*sp(a,c)*sp(b,c))%MOD)
#print(sp(1,2))
#print(sp(2,2))
#print()