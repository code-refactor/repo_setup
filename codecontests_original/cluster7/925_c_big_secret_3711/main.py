#!/usr/bin/env python3

n=int(input())
s=[[] for i in range(60)]
for b in list(map(int,input().split())):
	for i in range(59,-1,-1):
		if b>>i&1:
			s[i].append(b)
			break
ans=[]
cur=0
for i in range(n):
	fl=False
	for j in range(60):
		if s[j]!=[] and cur>>j&1==0:
			ans.append(s[j][-1])
			cur^=s[j][-1]
			s[j].pop()
			fl=True
			break
	if not fl:
		print('No')
		exit()
print('Yes')
print(' '.join(str(i) for i in ans))