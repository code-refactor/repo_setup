#!/usr/bin/env python3

from sys import stdin
inp = lambda: stdin.readline().strip()

n = int(inp())


def dfs(visited, graph, node):
    if not visited[node]:
        visited[node] = True
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)


adj = [set() for x in range(26)]
visited = [True]*26
for i in range(n):
    s = list(set(inp()))
    for j in range(len(s)):
        visited[ord(s[j])-97] = False
        for k in range(len(s)):
            if s[k] != s[j]:
                adj[ord(s[j])-97].add(ord(s[k])-97)

for i in range(26):
    adj[i] = list(adj[i])
counter = 0
for i in range(26):
    if not visited[i]:
        dfs(visited,adj,i)
        counter += 1
print(counter)