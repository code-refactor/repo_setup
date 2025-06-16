#!/usr/bin/env python3

from sys import stdin
input=lambda : stdin.readline().strip()
from math import ceil,sqrt,factorial,gcd
for _ in range(int(input())):
	n,k=map(int,input().split())
	if k>=n:
		print(1)
	else:
		l=[]
		s=int(sqrt(n))
		for i in range(2,s+2):
			if n%i==0 and i<=k:
				l.append(n//i)
				t=n//i
				if t<=k:
					l.append(n//t)
		if len(l)==0:
			print(n)
		else:
			print(min(l))