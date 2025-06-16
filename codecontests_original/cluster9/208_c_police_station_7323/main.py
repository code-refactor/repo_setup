#!/usr/bin/env python3

#build the graph with n cities and m roads
#figure out all of the shortest paths from city 1 to city n
#best=number of shortest paths (if we have police station at 1 or n)


s=list(map(int,input().split()))
n=s[0]
m=s[1]
roads=[]
Adj=[]
for i in range(0,n+1):
    roads.append([])
    Adj.append([False]*(n+1))
for i in range(0,m):
    s=list(map(int,input().split()))
    roads[s[0]].append(s[1])
    roads[s[1]].append(s[0])
    Adj[s[0]][s[1]]=True
    Adj[s[1]][s[0]]=True


#we gotta count how many shortest paths from 1 to n
#first bfs to find the length of the shortest path
#in our bfs, all the nodes now have "levels" from 1
Dist=[200]*(n+1)
Q=[1]
Dist[1]=0
while len(Q)>0:
    curr=Q.pop(0)
    for nex in roads[curr]:
        if Dist[nex]==200: #not Visited
            Dist[nex]=Dist[curr]+1
            Q.append(nex)

Levels=[]
for l in range(0,100):
    Levels.append([])
    for p in range(1,n+1):
        if Dist[p]==l:
            Levels[l].append(p)

#given a point p, paths[a][p]=sigma(paths[a][v]) where v is all of the points
#   on a level lower than p, connected to p
fromOne=[0]*(n+1)
def fo(b):
    """how many shortest paths from 1 to b"""
    if fromOne[b]>0:
        return fromOne[b]
    if b==1:
        return 1
    ans=0
    for p in Levels[Dist[b]-1]:
        if Adj[p][b]:
            ans+=fo(p)
    fromOne[b]=ans
    return ans

toN=[0]*(n+1)
def tN(b):
    """how many shortest paths from 1 to b"""
    if toN[b]>0:
        return toN[b]
    if b==n:
        return 1
    ans=0
    for p in Levels[Dist[b]+1]:
        if Adj[p][b]:
            ans+=tN(p)
    toN[b]=ans
    return ans

#OHHH we count how many shortest paths include policeStation
best=fo(n)
for policeStation in range(2,n):
    safe=fo(policeStation)*tN(policeStation)*2
    best=max(best,safe)
print(round(best/fo(n),10))

					 	  				 		  		 	 	 				