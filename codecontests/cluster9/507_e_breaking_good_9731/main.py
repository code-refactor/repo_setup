#!/usr/bin/env python3

from collections import deque

def bfs(n, v, s, t):
    dis = [n] * n
    load = [n] * n
    path = [None] * n
    q = deque([s])
    dis[s] = 0
    load[s] = 0
    while (q):
        node = q.popleft()
        for i in range(len(v[node])):
            nb = v[node][i][0]
            status = v[node][i][1]
            tmp_dis = dis[node] + 1
            tmp_load = load[node] + (status != 1)
            if ((tmp_dis, tmp_load) < (dis[nb], load[nb])):
                dis[nb] = tmp_dis
                load[nb] = tmp_load
                path[nb] = node
                if (node != t): q.append(nb)
        if (node == t):
            break
    node = t
    opt = set()
    while (node != s):
        opt.add((min(node, path[node]), max(node, path[node])))
        node = path[node]
    return dis[t], load[t], opt

#def sp(s, t):
    ## dijkstra
    #global m, n, v, st, l_min, w_min, opt
    #current = s
    #visited = set([s])
    #dis = {}
    #dis[s] = 0
    #path = [[] for _ in xrange(n)]
    #path[s] = [[]]
    #load = [[] for _ in xrange(n)]
    #load[s] = [0]
    #while (current != t):
        #if (debug >= 2):
            #print 'current=%d' % current
        #for i in xrange(len(v[current])):
            #nb = v[current][i]
            #status = st[current][i]
            #if (debug >= 2):
                #print ' nb=%d, st=%d:' % (nb, status),
            #if (not dis.has_key(nb) or dis[nb] > 1 + dis[current]):
                ## update
                #dis[nb] = 1 + dis[current]
                #load[nb] = []
                #path[nb] = []
                #for j in xrange(len(load[current])):
                    #path[nb].append(path[current][j][:])
                    #path[nb][j].append((current, nb))
                    #if (status == 0):
                        #load[nb].append(load[current][j] + 1)
                    #else:
                        #load[nb].append(load[current][j])
                #if (debug >= 2):
                    #print 'Updated'
            #elif (dis[nb] == 1 + dis[current]):
                ## append
                #for j in xrange(len(load[current])):
                    #path[nb].append(path[current][j][:])
                    #path[nb][len(path[nb]) - 1].append((current, nb))
                    #if (status == 0): load[nb].append(1 + load[current][j])
                    #else: load[nb].append(load[current][j])
                #if (debug >= 2):
                    #print 'Appended'
            #else:
                #if (debug >= 2):
                    #print 'Passed'
        #sorted_idx = sorted(dis, key = dis.get)
        #if (debug >= 2): print sorted_idx
        #idx = 0
        #while (sorted_idx[idx] in visited): idx += 1
        #current = sorted_idx[idx]
        #visited.add(current)
    #w_min = min(load[t])
    #l_min = dis[t]
    #opt = tuple(path[t][load[t].index(w_min)])
    #return 0

#def dfs(s, t, visited, path, l, w):
    #global m, n, v, st, l_min, w_min, opt
    ##print path
    #if (s == t):
        #if (l < l_min):
            #l_min = l
            #w_min = w
            #opt = tuple(path)
        #else:
            #if (w < w_min):
                #w_min = w
                #opt = tuple(path)
        #return 0
    #if (l >= l_min): return 0
    ##if (w >= w_min): return 0
    #for i in xrange(len(v[s])):
        #if (v[s][i] in visited): continue
        #visited.add(v[s][i])
        #path.append((s, v[s][i]))
        #if (st[s][i] == 1):
            #dfs(v[s][i], t, visited, path, l + 1, w)
        #else:
            #dfs(v[s][i], t, visited, path, l + 1, w + 1)
        #visited.remove(v[s][i])
        #path.pop(len(path) - 1)
    #return 0

global debug
debug = 0

#global m, n, v, st, l_min, w_min
n, m = list(map(int, input().split()))
#e = []
v = [[] for _ in range(n)]
a = 0 # bad count
b = 0 # good count
#l_min = n
#w_min = n
#opt = ()
for i in range(m):
    v1, v2, status = list(map(int, input().split()))
    if (status == 0): a += 1
    else: b += 1
    v[v1 - 1].append((v2 - 1, status))
    v[v2 - 1].append((v1 - 1, status))
    #e.append((v1, v2, status))
if (debug >= 1): t0 = time.time()
#dfs(0, n - 1, set(), [], 0, 0)
#sp(n - 1, 0)
#sp(0, n - 1)
l_min, w_min, opt = bfs(n, v, 0, n - 1)
#l_min, w_min, opt = bfs(n, v, st, n - 1, 0)
print(b - l_min + 2 * w_min)
#print opt
#for i in xrange(len(e)):
#    if ((e[i][0] - 1, e[i][1] - 1) in opt or (e[i][1] - 1, e[i][0] - 1) in opt):
#        if (e[i][2] == 0): print '%d %d 1' % (e[i][0], e[i][1])
#    else:
#        if (e[i][2] == 1): print '%d %d 0' % (e[i][0], e[i][1])
#for i in xrange(len(e)):
#    if ((min(e[i][0] - 1, e[i][1] - 1), max(e[i][0] - 1, e[i][1] - 1)) in opt):
#        if (e[i][2] == 0): print '%d %d 1' % (e[i][0], e[i][1])
#    else:
#        if (e[i][2] == 1): print '%d %d 0' % (e[i][0], e[i][1])
for v1 in range(n):
    for v2, status in v[v1]:
        if (v2 < v1): continue
        if ((v1, v2) in opt):
            if (status == 0): print('%d %d 1' % (v1 + 1, v2 + 1))
        else:
            if (status == 1): print('%d %d 0' % (v1 + 1, v2 + 1))
if (debug >= 1): print('%f' % (time.time() - t0))
