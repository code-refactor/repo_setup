from library import *

n, k = ints()
nodes = [[] for _ in range(n+1)]
edges = []

for node, dist in enumerate(ints()):
    nodes[dist].append(node)

if len(nodes[0]) != 1 or len(nodes[1]) > k:
    print(-1)
else:
    for i in range(1, n):
        if len(nodes[i])*(k-1) < len(nodes[i+1]):
            print(-1)
            exit()
    
    for i in range(n):
        next_idx = 0
        
        if len(nodes[i+1]) > 0:
            for j, node in enumerate(nodes[i]):
                current = 0
                
                while current < (k if i == 0 else k-1) and next_idx < len(nodes[i+1]):
                    edges.append((node+1, nodes[i+1][next_idx]+1))
                    next_idx += 1
                    current += 1

    print(len(edges))
    for u, v in edges:
        print(u, v)
