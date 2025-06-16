from library import *

n = int_inp()
respect = [0] * n
child_respect = [0] * n
root = -1

for i in range(n):
    p, c = ints()
    if p == -1:
        root = i
        continue
    respect[i] = c
    if p != -1 and not c:
        child_respect[p-1] = 1

res = []
for i in range(n):
    if i == root:
        continue
    if respect[i] and not child_respect[i]:
        res.append(i+1)

print(*res if res else [-1])