#!/usr/bin/env python3

from library import int_inp

n = int_inp()
children = [[] for _ in range(n+1)]
is_nonleaf = [False] * (n+1)

for i in range(2, n+1):
    parent = int_inp()
    children[parent].append(i)
    is_nonleaf[parent] = True

def count_leaf_children(node):
    if not children[node]:
        return 0
    
    leaf_count = 0
    for child in children[node]:
        if not is_nonleaf[child]:
            leaf_count += 1
        else:
            leaf_count += count_leaf_children(child)
    return leaf_count

for node in range(1, n+1):
    if is_nonleaf[node]:
        direct_leaves = sum(1 for child in children[node] if not is_nonleaf[child])
        if direct_leaves < 3:
            print("No")
            exit()

print("Yes")