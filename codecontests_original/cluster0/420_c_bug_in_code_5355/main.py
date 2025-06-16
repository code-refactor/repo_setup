#!/usr/bin/env python3

from collections import defaultdict
from bisect import bisect_left as lower
import sys
input = sys.stdin.readline
def put():
    return map(int, input().split())

try:
    n,m = put()
    cnt, mp, ans = [0]*n, defaultdict(), [0]*n
    for _ in range(n):
        x,y = put()
        x,y = x-1,y-1
        key = (min(x,y), max(x,y))
        if key in mp:
            mp[key]+=1
        else:
            mp[key]=1
        cnt[x]+=1
        cnt[y]+=1

except:
    print('lol')

for (x,y),val in mp.items():
    if cnt[x]+cnt[y]>= m and cnt[x]+cnt[y]-val<m:
        ans[x]-=1
        ans[y]-=1


scnt = cnt.copy()
scnt.sort()
for i in range(n):
    ans[i]+= n-lower(scnt, m-cnt[i])
    if 2*cnt[i]>=m:
        ans[i]-=1

print(sum(ans)//2)
