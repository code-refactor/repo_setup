#!/usr/bin/env python3

from library import FastIO

k, n, m = FastIO.read_ints()
a = FastIO.read_ints()
skill = []
l = [[[], [], []] for i in range(k)]
for j in range(n):
	t = FastIO.read_ints()
	skill.append(t)
	(t, i, b) = t
	l[i-1][t-1].append((b, j+1))
for i in range(k):
	for j in range(3):
		l[i][j].sort(reverse=True)
op = []
for i in range(k):
	t = l[i][1][:]
	if len(l[i][0]) != 0 and l[i][0][0][0] > a[i]:
		t.append((l[i][0][0][0] - a[i], l[i][0][0][1]))
		t.sort(reverse=True)
	s = a[i]
	for (add, index) in t:
		op.append(((s+add)/s, index))
		s += add
	for (mul, index) in l[i][2]:
		op.append((mul, index))
op.sort(reverse=True)
st = set(map(lambda t : t[1], op[:m]))
print(len(st))
for i in range(k):
	for j in range(3):
		for (mul, index) in l[i][j]:
			if index in st:
				print(index, end=' ')
