#!/usr/bin/env python3

INF = 10e9
n,s,k = map(int, input().split())
r = list(map(int, input().split()))
r.append(0)
col = input()
mat = []
for i in range(n+1):
    adj = {}
    for j in range(n):
        if i == n:
            adj[j] = abs((s-1)-j)
        else:
            if col[i] != col[j] and r[i] < r[j]:
                adj[j] = abs(i-j)
    mat.append(adj)
# print(*mat, sep='\n')

mem = [{} for i in range(n+1)]
# print(mem)

def get(s, k):
    # print(s,k)
    # print(mem)
    if mem[s].get(k):
        return mem[s].get(k)
    if r[s] >= k:
        mem[s][k] = 0
    else:
        mi = None
        for nei in mat[s]:
            ncost = get(nei, k-r[s])
            if ncost is None:
                continue
            curr = ncost + mat[s][nei]
            if mi is None or curr < mi:
                mi = curr
        if mi is not None:
            mem[s][k] = mi
        else:
            mem[s][k] = INF
    return mem[s].get(k)

# print(mem)

ans = get(n,k)
if ans is None or ans >= INF:
    print(-1)
else:
    print(ans)
