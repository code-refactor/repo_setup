#!/usr/bin/env python3

from library import ints, adj_list, subtree_sizes, run_with_threading

def main():
    n = int(input())
    if n % 2 != 0:
        print(-1)
        return
    
    edges = []
    for _ in range(n-1):
        x, y = ints()
        edges.append((x-1, y-1))
    
    graph = adj_list(n, edges)
    sizes = subtree_sizes(graph, 0)
    
    result = 0
    for i in range(1, n):
        if sizes[i] % 2 != 0:
            result += 1
    
    print(result)

run_with_threading(main)