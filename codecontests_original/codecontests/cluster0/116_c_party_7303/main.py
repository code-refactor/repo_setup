#!/usr/bin/env python3

def findDepth(a, i):
    depth = 1
    nextLevel = a[i][:]

    while len(nextLevel) > 0:
        depth += 1

        children = nextLevel[:]

        nextLevel = []

        for child in children:
            nextLevel += a[child]

    return depth




n = int(input())


a = []
for i in range(n):
    a.append([])


roots = []

for i in range(n):
    
    x = int(input())

    if x > 0:
        a[x-1].append(i)

    else:
        roots.append(i)


print(max([findDepth(a, i) for i in roots]))
    
