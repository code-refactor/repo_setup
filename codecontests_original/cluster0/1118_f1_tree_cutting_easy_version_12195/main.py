#!/usr/bin/env python3

import sys
input=sys.stdin.readline
n = int(input())
a = [int(t) for t in input().split(' ')]
mx = [[] for _ in range(n)]
for i in range(n-1):
    v1, v2 = map(int,input().split())
    mx[v1-1].append(v2-1)
    mx[v2-1].append(v1-1)
count = [[0, 0] for _ in range(n)]
total = [a.count(1), a.count(2)]
answer = 0
OBSERVE = 0
CHECK = 1
stack = [(OBSERVE, 0, -1)]
while len(stack):
    #print(stack,count)
    state, vertex, parent = stack.pop()
    if state == OBSERVE:
        stack.append((CHECK, vertex, parent))
        for child in mx[vertex]:
            #print(nv,v,from_)
            if child != parent:
                stack.append((OBSERVE, child, vertex))
    else:
        for child in mx[vertex]:
            if child != parent:
                #print(child,parent,count)
                if count[child][0] == total[0] and count[child][1] == 0 or count[child][1] == total[1] and count[child][0] == 0:
                    answer += 1
                count[vertex][0] += count[child][0]
                count[vertex][1] += count[child][1]
 
        if a[vertex] != 0:
            #print(count)
            count[vertex][a[vertex]-1] += 1
            #print(count)
 
print(answer)
