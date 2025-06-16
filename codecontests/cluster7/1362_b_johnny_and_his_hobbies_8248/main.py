#!/usr/bin/env python3
from library import read_array

t = int(input())
for T in range(t):
	n = int(input())
	lista = read_array(n)
	ma = max(lista)
	mi = min(lista)
	listb = [0] * n
	ans = 0
	lista_set = set(lista)  # Convert to set for faster lookup
	for k in range(1, 2 * ma + 1):
		temp = 0
		for i in range(n):
			listb[i] = lista[i] ^ k
			if listb[i] not in lista_set:
				temp = 1
				break
		if temp == 0:
			ans = 1
			print(k)
			break
	if ans == 0:
		print(-1)