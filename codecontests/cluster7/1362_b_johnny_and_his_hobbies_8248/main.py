#!/usr/bin/env python3

t=int(input())
for T in range(t):
	n=int(input())
	lista=[int(x) for x in input().split()]
	ma=max(lista)
	mi=min(lista)
	listb=[0]*n
	ans=0
	for k in range(1,2*ma+1):
		temp=0
		for i in range(n):
			listb[i]=lista[i]^k
			tk=0
			if(listb[i] not in lista):
				temp=1
				break
		if(temp==0):
			ans=1
			print(k)
			break
	if(ans==0):
		print(-1)