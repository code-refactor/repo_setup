from library import *
import re

def is_lucky(num):
    return re.fullmatch("[47]+", num) is not None

n = int_inp()
edges = []
for _ in range(n - 1):
    s = input().split()
    u, v = int(s[0]) - 1, int(s[1]) - 1
    c = is_lucky(s[-1])
    edges.append((u, v, c))

# Build weighted adjacency list where weight is boolean (lucky or not)
gr = [[] for _ in range(n)]
for u, v, c in edges:
    gr[u].append((v, c))
    gr[v].append((u, c))

# Custom topological order with edge costs
def topo_order_with_costs(graph, root):
    res = [(root, None, None)]
    i = 0
    while i < len(res):
        u, p, _ = res[i]
        i += 1
        for v, c in graph[u]:
            if v != p:
                res.append((v, u, c))
    return reversed(res)

topo = list(topo_order_with_costs(gr, 0))

# Calculate subtree sizes
tree_size = [1] * n
for u, p, _ in topo:
    if p is not None:
        tree_size[p] += tree_size[u]

# DP up and down
dp_up, dp_down = [0] * n, [0] * n
for u, p, cost in topo:
    if p is not None:
        dp_up[p] += tree_size[u] if cost else dp_up[u]

for u, p, cost in reversed(topo):
    if p is not None:
        dp_down[u] += tree_size[0] - tree_size[u] if cost else dp_down[p] + dp_up[p] - dp_up[u]

ans = sum(((u + v) * (u + v - 1) for u, v in zip(dp_up, dp_down)))
print(ans)
