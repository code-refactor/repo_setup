#!/usr/bin/env python3

from library import parse_int, parse_ints, count_degrees

# Read input
n = parse_int()
flag = True

# Create arrays to store edges and node degrees
edges = []
node_degrees = [0] * n

# Read the edges and calculate degrees
for _ in range(n - 1):
    u, v = parse_ints()
    edges.append((u, v))
    node_degrees[u - 1] += 1
    node_degrees[v - 1] += 1

# Find central node and endpoints
mid = 0
endpoints = []

for i in range(n):
    if node_degrees[i] == 1:
        # This is a leaf node/endpoint
        endpoints.append(i + 1)
    elif node_degrees[i] > 2:
        # This is a potential central node
        if mid == 0:
            mid = i + 1
        else:
            # More than one node with degree > 2 means no valid decomposition
            print("No")
            flag = False
            break

# If we found a valid decomposition
if flag:
    print("Yes")
    if mid != 0:
        # Star-like decomposition with central node
        print(len(endpoints))
        for endpoint in endpoints:
            if endpoint != mid:
                print(mid, endpoint)
    else:
        # Line-like decomposition with just two endpoints
        print(1)
        print(endpoints[0], endpoints[1])