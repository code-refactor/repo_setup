from library import *

# Fast input setup
input = fast_input()
n = int(input())
c, root = [], 0
graph = defaultdict(list)

for i in range(n):
    a, b = map(int, input().split())
    if a != 0:
        graph[i+1].append(a)
        graph[a].append(i+1)
    else:
        root = i+1
    c.append(b)

ans = [0] * (n + 1)
store = [[] for _ in range(n + 1)]

# Special case for n=1
if n == 1 and c[0] == 0:
    print('YES')
    print('1')
else:
    # Use iterative DFS pattern
    OBSERVE, CHECK = 0, 1
    stack = [(OBSERVE, root, 0)]
    ok = True
    
    while stack:
        state, vertex, parent = stack.pop()
        if state == OBSERVE:
            stack.append((CHECK, vertex, parent))
            for child in graph[vertex]:
                if child != parent:
                    stack.append((OBSERVE, child, vertex))
        else:
            i = 0
            while i < len(graph[vertex]):
                if graph[vertex][i] != parent:
                    if len(graph[graph[vertex][i]]) == 1 and graph[vertex][i] != root:
                        store[graph[vertex][i]].append([i+1, graph[vertex][i]])
                    store[vertex] += store[graph[vertex][i]]
                i += 1
            
            store[vertex].sort()
            
            if c[vertex-1] > len(store[vertex]):
                ok = False
                break
            else:
                if len(store[vertex]) > 0:
                    if c[vertex-1] != 0:
                        store[vertex].insert(c[vertex-1], [store[vertex][c[vertex-1]-1][0]+1, vertex])
                    else:
                        store[vertex].insert(c[vertex-1], [store[vertex][c[vertex-1]][0], vertex])
                for ijk in range(len(store[vertex])):
                    store[vertex][ijk][0] = ijk + 1
    
    if ok:
        for ij in store[root]:
            ans[ij[1]] = ij[0]
        print('YES')
        print(' '.join(map(str, ans[1:])))
    else:
        print('NO')
