#!/usr/bin/env python3

def dfs(s):
	stk,cnt=[],[]
	stk.append(s)
	cnt.append(0)
	while (len(stk)>0):
		s=stk[-1]
		ll=cnt[-1]
		visit[s]=1
		flag=1
		for j in range(ll,len(adj[s]),1):
			if visit[adj[s][j]]==0:
				cnt[-1]=j+1
				stk.append(adj[s][j])
				cnt.append(0)
				flag=0
				break
		if flag:
			stk.pop()
			cnt.pop()

n,m,d=map(int,input().split())
adj=[0]*(n+1)
for i in range(n+1):
	adj[i]=[]
for i in range(m):
	x,y=map(int,input().split())
	adj[x].append(y)
	adj[y].append(x)
visit=[0]*(n+1)
visit[1]=1
ans=[0]*m
ct=0
mark=[0]*(n+1)
mark[1]=1
for l in range(len(adj[1])):
	i=adj[1][l]
	if visit[i]==0:
		dfs(i)
		ans[ct]=[1,i]
		mark[i]=1
		ct+=1
if ct>d:
	print("NO")
	exit()
if ct<d:
	for i in range(len(adj[1])):
		if mark[adj[1][i]]==0:
			ans[ct]=[1,adj[1][i]]
			mark[adj[1][i]]=1
			ct+=1
		if ct==d:
			break
	if ct<d:
		print("NO")
		exit()
i=0
while (i<ct):
	k=ans[i][1]
	if visit[k]:
		# print(k,adj[k])
		for j in range(len(adj[k])):
			if mark[adj[k][j]]==0:
				mark[adj[k][j]]=1
				ans[ct]=[k,adj[k][j]]
				ct+=1
		visit[k]=0
	i+=1
print("YES")
for i in range(ct):
	print(*ans[i])