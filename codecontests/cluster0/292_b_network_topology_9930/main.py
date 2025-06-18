#!/usr/bin/env python3

from library import parse_ints

# Read input
n, m = parse_ints()

# Count the degree of each node (number of edges connected to it)
degrees = [0] * (n + 1)  # 1-indexed nodes

# Read m edges
for _ in range(m):
    a, b = parse_ints()
    degrees[a] += 1
    degrees[b] += 1

# Count nodes with each degree type
degree_1_count = 0  # Nodes with degree 1 (endpoints in a bus, leaves in a star)
degree_2_count = 0  # Nodes with degree 2 (middle nodes in a bus, all nodes in a ring)
degree_n_minus_1_count = 0  # Nodes with degree n-1 (center of a star)

for i in range(1, n + 1):
    if degrees[i] == 1:
        degree_1_count += 1
    elif degrees[i] == 2:
        degree_2_count += 1
    elif degrees[i] == n - 1:
        degree_n_minus_1_count += 1

# Determine the topology
if degree_1_count == 2 and degree_2_count == n - 2:
    print("bus topology")
elif degree_2_count == n:
    print("ring topology")
elif degree_1_count == n - 1 and degree_n_minus_1_count == 1:
    print("star topology")
else:
    print("unknown topology")