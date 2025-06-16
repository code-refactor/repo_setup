#!/usr/bin/env python3

def dfs(node, my_cc):
    vis[node] = True
    acc[my_cc]+=1
    for i in adj[node]:
        if not vis[i]:
            dfs(i, my_cc)

def ittDfs(node):
    queue = [node]
    curr = 0
    while(queue):
        node = queue.pop()
        if vis[node]:
            continue
        vis[node] = True
        acc[cc] += 1
        for i in adj[node]:
            if not vis[i]:
                queue.append(i)

def bfs(node):
	vis[node] = True
	cola = [node]

	cur = 0

	while (cur < len(cola)):
		x = cola[cur]
		acc[cc] += 1
		cur += 1;

		for i in adj[x]:
			if not vis[i]:
				vis[i] = True
				cola.append(i)

            
if __name__ == '__main__':
    _input = input().split()
    n = int(_input[0])
    m = int(_input[1])
    k = int(_input[2])
    
    adj = []
    vis = []
    acc = []
    cc = 0
    for i in range(n):
        vis.append(False)
        adj.append([])
        acc.append(0)

    for i in range(m):
        _in2 = input().split()
        v = int(_in2[0]) - 1
        w = int(_in2[1]) - 1
        adj[v].append(w)
        adj[w].append(v)
        
    for i in range(n):
        if not vis[i]:
            # dfs(i, cc)
            ittDfs(i)
            cc+=1
    
    if cc == 1:
        print(1 % k)
        exit()
        
    ans = 1
    for i in range(cc - 2):
        ans = ans * n
        ans = ans % k
    for i in range(cc):
        ans = ans * acc[i]
        ans = ans % k
    print(ans)
        