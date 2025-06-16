from library import *
from bisect import bisect_left as lower

n, m = ints()
cnt, mp, ans = [0]*n, defaultdict(int), [0]*n

for _ in range(n):
    x, y = ints()
    x, y = x-1, y-1
    key = (min(x,y), max(x,y))
    mp[key] += 1
    cnt[x] += 1
    cnt[y] += 1

for (x,y), val in mp.items():
    if cnt[x] + cnt[y] >= m and cnt[x] + cnt[y] - val < m:
        ans[x] -= 1
        ans[y] -= 1

scnt = sorted(cnt)
for i in range(n):
    ans[i] += n - lower(scnt, m - cnt[i])
    if 2 * cnt[i] >= m:
        ans[i] -= 1

print(sum(ans) // 2)
