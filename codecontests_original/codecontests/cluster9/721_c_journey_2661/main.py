#!/usr/bin/env python3

n, m, T = map(int, input().split())
graph_a = [[] for _ in range(n+1)]
graph_b = [[] for _ in range(n+1)]

double_graph_a = [[0 for _ in range(n+1)] for _ in range(n+1)]
double_graph_b = [[0 for _ in range(n+1)] for _ in range(n+1)]
 
for i in range(m):
    u, v, t = map(int, input().split())
    graph_a[v].append(u)
    graph_b[v].append(t)
    if u == 1:
        double_graph_a[v][2] = t
        double_graph_b[v][2] = 1

next_n = n + 1
for i in range(3, next_n):
    for j in range(2, next_n):
        for a, b in enumerate(graph_a[j]):
            if double_graph_a[b][i-1]:
                dist = double_graph_a[b][i-1] + graph_b[j][a]
                if dist <= T and (not double_graph_a[j][i] or dist < double_graph_a[j][i]):
                    double_graph_a[j][i] = dist
                    double_graph_b[j][i] = b

start = n
stop = 0
step = -1
for i in range(start, stop, step):
    if double_graph_b[start][i]:
        break

res = [n]
while double_graph_b[res[-1]][i] != 1:
    res.append(double_graph_b[res[-1]][i])
    i -= 1

res += [1]
print(len(res))
print(' '.join(map(str, res[::-1])))