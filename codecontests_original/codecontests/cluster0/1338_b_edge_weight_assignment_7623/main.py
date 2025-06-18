#!/usr/bin/env python3

import sys
# try:
# 	sys.stdin = open('input.txt', 'r') 
# 	sys.stdout = open('output.txt', 'w')
# except:
# 	pass

input = sys.stdin.readline
def DFS(i):
	visited = {i:True}
	stack = [(i,0)]
	while len(stack)!=0:
		tail,depth = stack.pop(-1)
		flag = True
		for each in neigh[tail]:
			if each not in visited:
				visited[each] = True
				flag = False
				stack.append((each,depth+1))
		if flag:
			leafDepth.append(depth)


n = int(input())

neigh = [[] for i in range(n)]
l = []
for i in range(n - 1):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    neigh[a].append(b)
    neigh[b].append(a)
    l.append((a,b))
#Max
edges = set()
for a, b in l:
    if len(neigh[a]) == 1:
        a = -1
    if len(neigh[b]) == 1:
        b = -1
    if a > b:
        a, b = b, a
    edges.add((a,b))

MAX = len(edges)

#Min
leafDepth = []

DFS(0)
if (len(neigh[0])==1):
	MIN = 1 if all([True if i%2==0 else False for i in leafDepth]) else 3
else:
	MIN = 1 if all([True if i%2==0 else False for i in leafDepth]) or all([True if i%2==1 else False for i in leafDepth]) else 3
        
#Out
print(MIN, MAX)