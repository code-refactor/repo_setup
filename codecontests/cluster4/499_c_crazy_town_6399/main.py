#!/usr/bin/env python3

x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
n = int(input())
arr = []
for _ in range(n):
	a, b, c = map(int, input().split())
	arr.append((a,b,c))
res = 0
for i in arr:
	a, b, c = i
	if(b != 0):
		y00 = -c/b
		y01 = -(a+c)/b
		s1 = x1*(y01-y00)-(y1-y00)
		s2 = x2*(y01-y00)-(y2-y00)
		if(s1<0<s2 or s1>0>s2):
			res += 1
	else:
		x = -c/a
		if(x1<x<x2 or x1>x>x2):
			res += 1
print(res)