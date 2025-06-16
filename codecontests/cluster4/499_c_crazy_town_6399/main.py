#!/usr/bin/env python3

from library import read_ints, read_int

x1, y1 = read_ints()
x2, y2 = read_ints()
n = read_int()
arr = [tuple(read_ints()) for _ in range(n)]
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