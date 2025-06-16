from library import *

n = int_inp()
cs = [0] * (n + 1)
ps = [0] * (n + 1)
children = [[] for _ in range(n + 1)]

for i in range(1, n + 1):
    p, c = ints()
    ps[i] = p
    children[p].append(i)
    cs[i] = c

def sortDescendants(v):
    result = []
    pos = cs[v]
    for child in children[v]:
        result += sortDescendants(child)
    if len(result) < pos:
        print('NO')
        exit()
    result.insert(pos, v)
    return result

root = children[0][0]
order = sortDescendants(root)
a = [0] * n
for i, v in enumerate(order):
    a[v - 1] = i + 1
print('YES')
print(*a)
