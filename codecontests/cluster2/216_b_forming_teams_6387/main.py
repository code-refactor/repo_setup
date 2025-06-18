#!/usr/bin/env python3

from library import read_ints, create_adj_list

def find_odd_cycles(n, edges):
    """
    Find the number of students that need to go to the bench
    - Students in odd-length cycles can't be in the same team
    - Total number of students must be even to form two equal teams
    """
    # Build adjacency list
    adj = create_adj_list(n, edges, one_indexed=True)
    
    # Track which students are assigned to teams
    color = [-1] * (n+1)  # -1: not visited, 0/1: team assignment
    odd_cycles_count = 0
    
    def dfs(node, parent, c):
        """
        DFS to detect bipartite coloring
        Returns True if successful, False if odd cycle detected
        """
        color[node] = c
        
        for neighbor in adj[node]:
            if neighbor == parent:
                continue
                
            if color[neighbor] == -1:
                if not dfs(neighbor, node, 1-c):
                    return False
            elif color[neighbor] == c:
                # Found odd cycle
                return False
        
        return True
    
    # Process each connected component
    for i in range(1, n+1):
        if color[i] == -1:
            # Start a new component
            if not dfs(i, -1, 0):
                odd_cycles_count += 1
    
    # Calculate number of students to bench
    bench_count = odd_cycles_count
    
    # If remaining students count is odd, add one more to bench
    if (n - bench_count) % 2 == 1:
        bench_count += 1
    
    return bench_count

def main():
    n, m = read_ints()
    edges = []
    
    for _ in range(m):
        edges.append(tuple(read_ints()))
    
    result = find_odd_cycles(n, edges)
    print(result)

if __name__ == "__main__":
    main()