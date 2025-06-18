#!/usr/bin/env python3

def iterative_dfs(graph, start, path=[]):
    visited = {}
    for i in graph:
        visited[i] = []
    q=[start]
    while q:
        v=q.pop(0)
        if not visited[v]:
            visited[v] = True
            path=path+[v]
            q=graph[v]+q
    return path
    
nodes, edges = map(int, input().split(' '))
graph = {}
for i in range(nodes):
  graph[i] = []

for i in range(edges):
  a, b = map(int, input().split(' '))
  graph[a-1].append(b-1)
  graph[b-1].append(a-1)

marked = [False] * nodes
num = 0
for i in range(nodes):
  if not marked[i]:
    for j in iterative_dfs(graph, i):
      marked[j] = True
    num += 1
print(2**(nodes-num))
