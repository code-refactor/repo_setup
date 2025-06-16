from library import *

n, m = ints()
c = list(ints())
graph = defaultdict(set)

for _ in range(m):
    a, b = ints()
    if c[a-1] == c[b-1]:
        continue
    graph[c[a-1]].add(c[b-1])
    graph[c[b-1]].add(c[a-1])

d, f = min(c), 0
for color in sorted(graph):
    h = len(graph[color])
    if h > f:
        f = h
        d = color
print(d)