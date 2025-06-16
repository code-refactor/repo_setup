#!/usr/bin/env python3

from collections import  defaultdict
import threading
from sys import stdin,setrecursionlimit
setrecursionlimit(300000)
input=stdin.readline

def dfs(node,g,par,sz):
	for i in g[node]:
		if i!=par:
			sz[node]+=dfs(i,g,node,sz)
	return sz[node]+1
def main():
	n=int(input())
	if n%2!=0:
		print(-1)
		exit(0)
	g=defaultdict(list)
	for i in range(n-1):
		x,y=map(int,input().strip().split())
		g[x-1].append(y-1)
		g[y-1].append(x-1)

	sz=[0]*(n)
	tt=[]
	dfs(0,g,-1,sz)
	res=0
	# print(sz)
	for i in range(1,n):
		if sz[i]%2!=0:
			res+=1
	print(res)

threading.stack_size(10 ** 8)
t = threading.Thread(target=main)
t.start()
t.join()