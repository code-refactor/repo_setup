#!/usr/bin/env python3

import sys
sys.path.append('..')

input = sys.stdin.buffer.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        L = []; R = []
        for i in range(n):
            l,r = map(int,input().split())
            L.append(l); R.append(r)
        
        edges = []
        for i in range(n-1):
            a,b = map(int,input().split())
            edges.append((a, b))
        
        G = TreeBuilder.from_edges(n, edges)
        
        root = 0
        par = [-1]*n
        dp = [[0, 0] for _ in range(n)]
        
        def process_node(u, parent, adj):
            if parent == -1: return
            v = parent
            zero = max(dp[u][0] + abs(L[v] - L[u]), dp[u][1] + abs(L[v] - R[u]))
            one = max(dp[u][0] + abs(R[v] - L[u]), dp[u][1] + abs(R[v] - R[u]))
            dp[v][0] += zero
            dp[v][1] += one
        
        # Set up parent relationships manually since we need them in process_node
        stack = [(root, -1)]
        visited = [False] * n
        
        while stack:
            u, parent = stack[-1]
            if not visited[u]:
                visited[u] = True
                par[u] = parent
                for v in G[u]:
                    if v != parent:
                        stack.append((v, u))
            else:
                process_node(u, parent, G)
                stack.pop()
        
        ans = max(dp[0])
        print(ans)

if __name__ == "__main__":
    main()