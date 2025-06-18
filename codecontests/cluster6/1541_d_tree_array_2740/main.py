#!/usr/bin/env python3

from functools import lru_cache
from collections import deque
from library import read_int, read_ints, mod_add, mod_mul, mod_inverse, MOD1

# Dynamic programming function to calculate probability of inversions
@lru_cache(None)
def dp(u, v):
    """Calculate probability of inversions between nodes at given depths.
    
    Args:
        u: Depth of first node from the LCA
        v: Depth of second node from the LCA
    
    Returns:
        Probability that the node at depth u is marked before the node at depth v
    """
    # Base cases
    if u == 0:  # First node is at the LCA, so it must be marked first if second node is deeper
        return 0
    if v == 0:  # Second node is at the LCA, so first node must be marked after
        return 1
    
    # Recursive case - equal probability of either path
    inv_2 = mod_inverse(2, MOD1)  # 1/2 probability
    term1 = mod_mul(dp(u - 1, v), inv_2, MOD1)  # Mark a node closer to u
    term2 = mod_mul(dp(u, v - 1), inv_2, MOD1)  # Mark a node closer to v
    
    return mod_add(term1, term2, MOD1)

def calc_inversions_for_root(n, distances, start):
    """Calculate expected inversions when starting from a given root.
    
    Args:
        n: Number of nodes
        distances: Matrix of distances between nodes
        start: Root node to start from
    
    Returns:
        Expected number of inversions when starting from this root
    """
    result = 0
    
    # Iterate through all pairs of nodes
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            # Calculate the lowest common ancestor (LCA) depth
            lca_depth = (distances[start][u] + distances[start][v] - distances[u][v]) // 2
            
            # Calculate depths from LCA
            u_depth = distances[start][u] - lca_depth
            v_depth = distances[start][v] - lca_depth
            
            # Add probability of inversion for this pair
            result = mod_add(result, dp(u_depth, v_depth), MOD1)
    
    return result

def main():
    # Read input
    n = read_int()
    
    # Build the tree
    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = read_ints()
        graph[u].append(v)
        graph[v].append(u)
    
    # Calculate distances between all pairs of nodes using BFS
    distances = [[-1 for _ in range(n + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        # Distance to self is 0
        distances[i][i] = 0
        
        # BFS to calculate distances from node i to all other nodes
        queue = deque([i])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if distances[i][v] >= 0:  # Already visited
                    continue
                distances[i][v] = distances[i][u] + 1
                queue.append(v)
    
    # Calculate expected inversions by averaging over all possible starting nodes
    total_inversions = 0
    for root in range(1, n + 1):
        total_inversions = mod_add(total_inversions, 
                                  calc_inversions_for_root(n, distances, root), 
                                  MOD1)
    
    # Average by dividing by the number of nodes
    result = mod_mul(total_inversions, mod_inverse(n, MOD1), MOD1)
    
    print(result)

if __name__ == "__main__":
    main()
