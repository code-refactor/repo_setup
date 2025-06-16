#!/usr/bin/env python3

import sys
from array import array  # noqa: F401


def readline(): return sys.stdin.buffer.readline().decode('utf-8')


def build_bridge_tree(v_count, edge_count, adj, edge_index):
    from collections import deque

    preorder = [0]
    parent, order, low = [0]+[-1]*v_count, [0]+[-1]*(v_count-1), [0]*v_count
    stack = [0]
    rem = [len(dests)-1 for dests in adj]
    pre_i = 1

    while stack:
        v = stack.pop()

        while rem[v] >= 0:
            dest = adj[v][rem[v]]
            rem[v] -= 1

            if order[dest] == -1:
                preorder.append(dest)
                order[dest] = low[dest] = pre_i
                parent[dest] = v
                pre_i += 1
                stack.extend((v, dest))
                break

    is_bridge = array('b', [0]) * edge_count

    for v in reversed(preorder):
        for dest, ei in zip(adj[v], edge_index[v]):
            if dest != parent[v] and low[v] > low[dest]:
                low[v] = low[dest]
            if dest != parent[v] and order[v] < low[dest]:
                is_bridge[ei] = 1

    bridge_tree = [[] for _ in range(v_count)]
    stack = [0]
    visited = array('b', [1] + [0]*(v_count-1))

    while stack:
        v = stack.pop()
        dq = deque([v])
        while dq:
            u = dq.popleft()
            for dest, ei in zip(adj[u], edge_index[u]):
                if visited[dest]:
                    continue
                visited[dest] = 1

                if is_bridge[ei]:
                    bridge_tree[v].append(dest)
                    bridge_tree[dest].append(v)
                    stack.append(dest)
                else:
                    dq.append(dest)

    return bridge_tree


def get_dia(adj):
    from collections import deque
    n = len(adj)
    dq = deque([(0, -1)])

    while dq:
        end1, par = dq.popleft()
        for dest in adj[end1]:
            if dest != par:
                dq.append((dest, end1))

    prev = [-1]*n
    prev[end1] = -2
    dq = deque([(end1, 0)])

    while dq:
        end2, diameter = dq.popleft()
        for dest in adj[end2]:
            if prev[dest] == -1:
                prev[dest] = end2
                dq.append((dest, diameter+1))

    return end1, end2, diameter, prev


n, m = map(int, readline().split())
adj = [[] for _ in range(n)]
eindex = [[] for _ in range(n)]

for ei in range(m):
    u, v = map(int, readline().split())
    adj[u-1].append(v-1)
    adj[v-1].append(u-1)
    eindex[u-1].append(ei)
    eindex[v-1].append(ei)

btree = build_bridge_tree(n, m, adj, eindex)
print(get_dia(btree)[2])
