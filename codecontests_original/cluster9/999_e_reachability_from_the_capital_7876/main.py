#!/usr/bin/env python3

def main():
    import sys
    sys.setrecursionlimit(10**5)
    from collections import deque
    n, m, s = map(int, input().split())
    s -= 1
    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u-1].append(v-1)

    seen = [False]*n
    li = deque()

    def visit(node):
        if not seen[node]:
            seen[node] = True
            for c_node in graph[node]:
                visit(c_node)
            li.appendleft(node)

    def visit2(node):
        if not seen[node]:
            seen[node] = True
            for c_node in graph[node]:
                visit2(c_node)

    for i in range(n):
        visit(i)
    seen = [False]*n
    cnt = 0
    visit2(s)
    for i in li:
        if seen[i]:
            continue
        visit2(i)
        cnt += 1
    print(cnt)

if __name__ == "__main__":
    try:
        main()
    except:
        print('error!')
        exit(0)