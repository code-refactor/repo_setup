#!/usr/bin/env python3

n,m = map(int,input().split())
dic = {}
edges = []
from collections import Counter
def find(node):
    tmp = node
    while node!=dic[node]:
        node = dic[node]
    while tmp!=dic[tmp]:
        dic[tmp],tmp=node,dic[tmp]
    return node
for _ in range(m):
    p1,p2 = map(int,input().split())
    dic.setdefault(p1,p1)
    dic.setdefault(p2,p2)
    edges.append(p1)
    lp = find(p1)
    rp = find(p2)
    if lp!=rp:
        dic[rp] = lp
for k in dic:
    find(k)
def judge():
    counter = Counter([dic[i] for i in edges])
    s = Counter(dic.values())
    for k in counter:
        en,nn = counter[k],s[k]
        if (nn**2-nn)//2!=en:
            return False
    return True
if judge():
    print("YES")
else:
    print("NO")