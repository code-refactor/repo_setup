#!/usr/bin/env python3

n, k = map(int, input().split())
t = list(map(int, input()))

p, d = 1, 10**9 + 7
s = 0
f = [1] * n

for i in range(2, n):
	f[i] = (i * f[i - 1]) % d

c = lambda a, b: 0 if a > b else (f[b] * pow(f[a] * f[b -a], d - 2, d)) % d

if k:
	u = [0] * (n + 1)
	p = [1] * (n + 1)

	for i in range(n):
		u[i] = (p[i] * c(k - 1, n - 2 - i) + u[i - 1]) % d

		p[i + 1] = (10 * p[i]) % d

	for i in range(n):
		v = u[n - 2 - i] + p[n - 1 - i] * c(k,i)
		s = (s + t[i] * v) % d

else:
	for i in t:
		s = (s * 10 + i) % d

print(s)

#GG