#!/usr/bin/env python3

import sys
import threading
from collections import deque

def func():
    lines = sys.stdin.readlines()
    nxt = 0
    t = int(lines[nxt])
    nxt += 1
    ans = []
    for _ in range(t):
        n,m,a,b = map(int, lines[nxt].split())
        nxt += 1
        g = [[] for _ in range(n)]
        for _ in range(m):
            u,v = map(int, lines[nxt].split())
            nxt += 1
            g[u-1].append(v-1)
            g[v-1].append(u-1)
        a -= 1
        b -= 1
        sigs = [0]*n
        sigs[a] = -1
        sigs[b] = -1
        cur_sig = 0
        inv = {}
        cnt = {}
        for i in range(n):
            if sigs[i]:
                continue
            cur_sig += 1
            cnt[cur_sig] = 1
            inv[cur_sig] = set()
            sigs[i] = cur_sig
            q = deque()
            q.append(i)
            while len(q):
                node = q.popleft()
                # if node == a:
                #     inv[cur_sig].add("A")
                # if node == b:
                #     inv[cur_sig].add("B")
                # if sigs[node]:
                #     continue
                # sigs[node] = cur_sig
                # cnt[cur_sig] += 1
                for v in g[node]:
                    if v == a:
                        inv[cur_sig].add("A")
                    if v == b:
                        inv[cur_sig].add("B")
                    if sigs[v]:
                        continue
                    sigs[v] = cur_sig
                    cnt[cur_sig] += 1
                    q.append(v)
        A = 0
        B = 0
        for k,v in inv.items():
            if v == {"A"}:
                A += cnt[k]
            if v == {"B"}:
                B += cnt[k]
        ans.append(str(A*B))
    print("\n".join(ans))
            

func()
        
        
        
            
        
        
    
        

