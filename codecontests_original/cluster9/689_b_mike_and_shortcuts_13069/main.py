#!/usr/bin/env python3

def amount_of_total_energy(n, a):
    dist = [-1] * n
    dist[0] = 0
    pos = [0]

    for u in pos:
	    for v in [u - 1, u + 1, a[u] - 1]:
		    if v >= 0 and v < n and dist[v] == -1:
			    dist[v] = dist[u] + 1
			    pos.append(v)	
    
    return dist

n = int(input())
a = list(map(int,input().split()))

print(*amount_of_total_energy(n, a))