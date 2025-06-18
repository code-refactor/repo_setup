#!/usr/bin/env python3

from library import parse_int, is_lucky
from sys import stdin

def topo_order(adj_list, start):
    """Get a topological ordering of nodes with parent info.
    
    Args:
        adj_list: Adjacency list where each entry contains (node, is_lucky_edge) tuples
        start: Starting node
        
    Returns:
        List of (node, parent, edge_cost) tuples in reverse topological order
    """
    res = [(start, None, None)]
    i = 0
    while i < len(res):
        node, parent, _ = res[i]
        i += 1
        for neighbor, cost in adj_list[node]:
            if neighbor != parent:
                res.append((neighbor, node, cost))
    return reversed(res)

def main():
    n = parse_int()
    
    # Initialize the adjacency list
    graph = [[] for _ in range(n)]
    
    # Read edges
    for _ in range(n - 1):
        s = stdin.readline().split()
        u, v = int(s[0]) - 1, int(s[1]) - 1  # Convert to 0-indexed
        c = is_lucky(s[-1])  # Check if the weight is lucky
        
        # Add edges to the graph (undirected)
        graph[u].append((v, c))
        graph[v].append((u, c))
    
    # Get nodes in topological order with parent info
    topo = list(topo_order(graph, 0))

    # Calculate subtree sizes
    tree_size = [1 for _ in range(n)]
    for u, p, _ in topo:
        if p is not None:
            tree_size[p] += tree_size[u]

    # Dynamic programming for paths
    dp_up = [0 for _ in range(n)]    # Count paths going up from node
    dp_down = [0 for _ in range(n)]  # Count paths going down to node
    
    # Process nodes bottom-up
    for u, p, cost in topo:
        if p is not None:
            dp_up[p] += tree_size[u] if cost else dp_up[u]

    # Process nodes top-down
    for u, p, cost in reversed(topo):
        if p is not None:
            dp_down[u] += tree_size[0] - tree_size[u] if cost else dp_down[p] + dp_up[p] - dp_up[u]

    # Calculate final answer: sum of (a+b)*(a+b-1) for each node's paths
    ans = sum(((u + v) * (u + v - 1) for u, v in zip(dp_up, dp_down)))
    print(ans)

if __name__ == "__main__":
    main()
