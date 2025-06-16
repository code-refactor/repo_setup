#!/usr/bin/env python3

def build_graph():
    line1 = input().strip().split()
    n = int(line1[0])
    m = int(line1[1])
    graph = {}
    for _ in range(m):
        line = input().strip().split()
        u = int(line[0])
        v = int(line[1])
        c = int(line[2])
        if c not in graph:
            graph[c] = {j: [] for j in range(1, n+1)}
        graph[c][u].append(v)
        graph[c][v].append(u)
    return graph

def no_of_paths(u, v, graph):
    x = 0
    for c in graph:
        parent = {}
        parent = dfs_visit(v, graph[c], parent)
        if u in parent:
            x += 1
    return x

def dfs_visit(i, adj_list, parent):
    for j in adj_list[i]:
        if j not in parent:
            parent[j] = i
            dfs_visit(j, adj_list, parent)
    return parent


if __name__ == "__main__":
    graph = build_graph()
    for _ in range(int(input())):
        line = input().strip().split()
        print(no_of_paths(int(line[0]), int(line[1]), graph))