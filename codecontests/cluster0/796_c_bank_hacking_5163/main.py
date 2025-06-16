from library import *

n = int_inp()
arr = list(ints()) + [-int(1e9+3)]
c = Counter(arr)
top, sec = sorted(set(arr))[-1:-3:-1]
top_cnt = [int(i == top) for i in arr]
sec_cnt = [int(i == sec) for i in arr]

edges = []
for _ in range(n-1):
    u, v = ints()
    edges.append((u, v))

for u, v in edges:
    if arr[u-1] == top: top_cnt[v-1] += 1
    if arr[v-1] == top: top_cnt[u-1] += 1
    if arr[u-1] == sec: sec_cnt[v-1] += 1
    if arr[v-1] == sec: sec_cnt[u-1] += 1

res = top + 2
for i in range(n):
    if top_cnt[i] < c[top]: 
        continue
    if top_cnt[i] == 1 and arr[i] == top:
        curr = top  
    else: 
        curr = top+1 
    if sec_cnt[i] < c[sec]: 
        curr = max(curr, sec+2)
    res = min(res, curr)
print(res)
