#!/usr/bin/env python3

from sys import stdin
input=lambda : stdin.readline().strip()

def get_divisors(n):
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(divisors)

for _ in range(int(input())):
	n,k=map(int,input().split())
	if k>=n:
		print(1)
	else:
		divisors = get_divisors(n)
		l=[]
		for d in divisors:
			if d <= k:
				l.append(n//d)
		if len(l)==0:
			print(n)
		else:
			print(min(l))