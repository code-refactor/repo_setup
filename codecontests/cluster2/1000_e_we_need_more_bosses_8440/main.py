#!/usr/bin/env python3

from library import build_bridge_tree, find_diameter, read_ints, read_graph, create_adj_list

n, m = read_ints()
edges = []
eindex = [[] for _ in range(n)]

for ei in range(m):
    u, v = read_ints()
    edges.append((u, v))

# Create adjacency list with proper indexing
adj = create_adj_list(n, [(u-1, v-1) for u, v in edges], one_indexed=False)

# Prepare edge indices for bridge tree construction
for ei, (u, v) in enumerate(edges):
    eindex[u-1].append(ei)
    eindex[v-1].append(ei)

# Build bridge tree and find its diameter
btree = build_bridge_tree(adj, eindex)
print(find_diameter(btree)[2])