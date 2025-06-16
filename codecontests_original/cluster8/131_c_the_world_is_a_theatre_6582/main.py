#!/usr/bin/env python3

from sys import stdin, stdout
a, b, c = [int(a) for a in stdin.read().split()]
ZA = [1, 1]
for d in range(2, 31):
	ZA.append(d * ZA[d - 1])
e = 0
if c - b < 4:
	d = 4
else:
	d = c - b
while d <= a and d < c:
	e = e + ZA[a] // ZA[d] // ZA[a - d] * ZA[b] // ZA[c - d] // ZA[b - c + d]
	d = d + 1
stdout.write(str(e))
