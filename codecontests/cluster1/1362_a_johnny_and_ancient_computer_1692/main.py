#!/usr/bin/env python3

# from debug import debug
import math
t = int(input())

for ii in range(t):
	a, b = map(int, input().split())
	if a == b:
		print(0)
	else:
		b, a = min(a,b), max(a,b)
		if a%b:
			print(-1)
		else:
			aa = int(math.log2(a//b))
			if pow(2, aa) == a//b:
				c = 0
				c += aa//3
				aa = aa%3

				c += aa//2
				aa = aa%2

				c += aa//1
				aa = aa%1
				print(c)
			else:
				print(-1)
