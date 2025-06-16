#!/usr/bin/env python3

import sys
input = sys.stdin.buffer.readline

def main():
    t = int(input()); INF = float("inf")
    for _ in range(t):
        n = int(input())
        L = []; R = []
        for i in range(n):
            l,r = map(int,input().split())
            L.append(l); R.append(r)
        G = [[] for _ in range(n)]
        for i in range(n-1):
            a,b = map(int,input().split())
            a-=1;b-=1 #0-index
            G[a].append(b)
            G[b].append(a)

        root = 0
        #depth = [-1]*n
        #depth[0] = 0
        par = [-1]*n
        #depth_list = defaultdict(list)
        #depth_list[0].append(root)
        stack = []
        stack.append(~0)
        stack.append(0)
        dp = [[0, 0] for _ in range(n)]
        #cnt = 0
        while stack:
            #cnt += 1
            v = stack.pop()
            if v >= 0:
                for u in G[v]:
                    if u == par[v]: continue
                    par[u] = v
                    stack.append(~u)
                    stack.append(u)
            
            else:
                u = ~v #child
                v = par[u] #parent
                if v == -1: continue
                zero = max(dp[u][0] + abs(L[v] - L[u]), dp[u][1] + abs(L[v] - R[u]))
                one = max(dp[u][0] + abs(R[v] - L[u]), dp[u][1] + abs(R[v] - R[u]))
                dp[v][0] += zero
                dp[v][1] += one
        ans = max(dp[0])
        #print("CNT",cnt)
        #print(dp)
        print(ans)

if __name__ == "__main__":
    main()