#!/usr/bin/env python3

n, m = [int(x) for x in input().split()]
tps = {i:int(t) for i, t in enumerate(input().split())}
deps = {i:0 for i in range(n)}
parents = {i:[] for i in range(n)}
leafs = {i for i in range(n)}
for i in range(m):
    x, y = [int(x) for x in input().split()]
    deps[x] += 1
    parents[y].append(x)
    if x in leafs:
        leafs.remove(x)

deep = {i:tps[i] for i in range(n)}
res = 0
while len(leafs) > 0:
    leaf = leafs.pop()
    if len(parents[leaf])==0:
        res = max(res, deep[leaf])
        continue
##    print(leaf, leafs)
    for parent in parents[leaf]:
        l = deep[leaf]
        if tps[parent] == 1 and tps[leaf] == 0:
            l += 1
        if deep[parent] < l:
            deep[parent] = l
            
        deps[parent] -= 1
        if deps[parent] == 0:
            leafs.add(parent)
##        print(leaf, parent, l, deps[parent], leafs, deep)
    
    
print(res)
