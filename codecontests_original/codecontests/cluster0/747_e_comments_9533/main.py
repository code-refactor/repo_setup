#!/usr/bin/env python3

from queue import Queue

def parse(s):
    A = s.split(',')
    n = len(A)//2
    B = [(A[2*i], int(A[2*i+1])) for i in range(n)]

    stack = []
    E = {i:[] for i in range(n+1)}
    comment = {}
    depth = {i:0 for i in range(n+1)}
    for i, b in enumerate(reversed(B)):
        comment[i+1] = b[0]
        for j in range(b[1]):
            k = stack.pop()
            E[i+1].append(k)
            depth[i+1] = max(depth[i+1], depth[k])

        depth[i+1] += 1
        stack.append(i+1)

    E[0].extend(reversed(stack))
    depth[0] = max(depth[i] for i in stack) + 1
    comment[0] = None

    Q = Queue()
    Q.put(0)
    res = [[] for i in range(depth[0])]
    while not Q.empty():
        v = Q.get()
        d = depth[v] - 1
        res[d].append(comment[v])
        for u in E[v]:
            depth[u] = d
            Q.put(u)

    res.pop()
    return res

s = input().rstrip()
res = parse(s)    
print(len(res))
for layer in reversed(res):
    print(' '.join(layer))
