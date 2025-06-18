#!/usr/bin/env python3

import sys
import threading

def main():

    
    p = input().split()
    n = int(p[0]) #number of locations
    m = int(p[1]) #number of passages

    if n==1: #if there's only one location, there's nothing to do
        print(0)
        return
    if n==2: #if there's only two nodes, the only edge between them, is always a bridge
        print(-1)
        return

    g = graph(n,m)

    g.buildBridgeTree()
    
    e = graph(len(g.bridges)+1,len(g.bridges))

    e.conexions= []
    e.pi=[]
    e.discovery=[]
    e.seen=[]

    for i in range(len(g.bridges)+1):
        e.conexions.append([])
        e.pi.append(-1)
        e.discovery.append(sys.float_info.max)
        e.seen.append(False)
    for i in range(len(g.bridges)):
        e.conexions[g.cc[g.bridges[i][0]]].append((g.cc[g.bridges[i][1]],True))
        e.conexions[g.cc[g.bridges[i][1]]].append((g.cc[g.bridges[i][0]],True))
    
    e.bridges=g.bridges
    e.bridge=g.bridge
    e.cc=g.cc
    e.CC=e.CC
    e.CC

    e.treeDiameter()

    print(len(e.newEdges))
    for i in range(len(e.newEdges)):
        u = e.newEdges[i][0] +1
        v = e.newEdges[i][1] +1
        print(u, end=" ")
        print(v)

class graph:

    n = int() #number of nodes
    edges= int() #number of edges
    time = int() 


    conexions = [] #adjacency list
    bridges=[] #are we using a removable edge or not for city i?
    bridge=[]


    discovery = [] #time to discover node i
    seen = [] #visited or not
    cc = [] #index of connected components
    low = [] #low[i]=min(discovery(i),discovery(w)) w:any node discoverable from i
    pi = [] #index of i's father 

    CC = []
    newEdges = []

    def __init__(self, n, m):

        self.n = n
        self.edges = m

        for i in range(self.n):
            self.conexions.append([])
            self.discovery.append(sys.float_info.max)
            self.low.append(sys.float_info.max)
            self.seen.append(False)
            self.cc.append(-1)
            self.CC.append([])
            self.bridge.append([])
            
    
    def buildGraph(self):
        #this method put every edge in the adjacency list
        for i in range(self.edges):
            p2=input().split()
            self.conexions[int(p2[0])-1].append((int(p2[1])-1,False))
            self.conexions[int(p2[1])-1].append((int(p2[0])-1,False))
    
    def searchBridges (self):
        self.time = 0 

        for i in range(self.n):
            self.pi.append(-1)
            for j in range(self.n):
                self.bridge[i].append(False)
        
        


        self.searchBridges_(0,-1) #we can start in any node 'cause the graph is connected

    
    def searchBridges_(self,c,index):

        self.seen[c]=True #mark as visited
        self.time+=1
        self.discovery[c]=self.low[c]= self.time

        for i in range(len(self.conexions[c])):
        
            pos = self.conexions[c][i][0]
            if not self.seen[pos]:
                self.pi[pos]=c #the node that discovered it
            
                self.searchBridges_(pos,i) #search throw its not visited conexions
            
                self.low[c]= min([self.low[c],self.low[pos]]) #definition of low
            
            elif self.pi[c]!=pos: #It is not the node that discovered it
                self.low[c]= min([self.low[c],self.discovery[pos]])
        
        if self.pi[c]!=-1 and self.low[c]==self.discovery[c]:  #it isn't the root and none of its connections is reacheable earlier than it
            self.bridges.append((c,self.pi[c]))
            self.bridge[self.pi[c]][c]=self.bridge[c][self.pi[c]]= True
            
            for i in range(len(self.conexions[c])):
                if(self.conexions[c][i][0]==self.pi[c]):
                    self.conexions[c][i]=(self.pi[c],True)
                    self.conexions[self.pi[c]][index]=(c,True)

        
            
        


    def findCC(self):

        j = 0

        for i in range(self.n):
            self.pi[i]=-1
            self.seen[i]=False
        
        for i in range(self.n):
            if self.seen[i]==False:
                self.cc[i]=j #assign the index of the new connected component
                self.CC[j].append(i)
                self.findCC_(i,j) #search throw its not visited conexions
                j+=1 #we finished the search in the connected component
    
    def findCC_(self, c, j):

        self.seen[c]=True #mark as visited

        for i in range(len(self.conexions[c])):

            pos = self.conexions[c][i][0]
            if(self.seen[pos]==False and self.conexions[c][i][1]==False):
                
                self.cc[pos]=j #assign the index of the connected component
                self.CC[j].append(pos)
                self.pi[pos]=c #the node that discovered it
                self.findCC_(pos,j) #search throw its not visited conexions

    def treeDiameter(self):

       while self.n>1:

            for i in range(self.n):
                self.seen[i]=False
                self.pi[i]=-1
            self.discovery[0]=0
            self.treeDiameter_(0) #search the distance from this node, to the others
            max = -1
            maxIndex = 0
            for i in range(self.n):
                if self.discovery[i]>max:
                    max= self.discovery[i] #look for the furthest node
                    maxIndex=i
            for i in range(self.n):
                self.seen[i]=False
                self.pi[i]=-1
            self.discovery[maxIndex]=0
            self.treeDiameter_(maxIndex)  #search the distance from the furthest node, to the others
            max =-1
            maxIndex2=-1
            for i in range(self.n):
                if self.discovery[i]>max :
                    max= self.discovery[i] #look for the furthest node to preview furthest node, and that is the diameter in a tree
                    maxIndex2=i
        
            self.ReBuildTree(maxIndex,maxIndex2)


    def treeDiameter_(self, c):

        self.seen[c]=True #mark as visited

        for i in range(len(self.conexions[c])):

            pos = self.conexions[c][i][0]

            if self.seen[pos]==False:

                self.pi[pos]=c #the node that discovered it
                self.discovery[pos]= self.discovery[c]+1 #distance to the node who discover it + 1
                #we don't have to compare and search for other paths, since it's a tree and there is only one path between two nodes.
                self.treeDiameter_(pos) #search throw its not visited conex16 ions



    def buildBridgeTree(self):
        
        self.buildGraph()
        self.searchBridges()
        self.findCC()

    def ReBuildTree(self, u, v):
        find=0

        for i in range(len(self.CC[u])):
            for j in range(len(self.CC[v])):
                if not self.bridge[self.CC[u][i]][self.CC[v][j]]:
                    self.newEdges.append((self.CC[u][i],self.CC[v][j]))
                    find=1
                    break
            
            if find==1:
                break

        newIndex=[]
        temp = v
        self.conexions[u]=None
        self.conexions[v]=None

        while self.pi[temp]!=u:
            self.conexions[self.pi[temp]]=None
            temp = self.pi[temp]

        r =1
        for i in range(self.n):
            if(self.conexions[i]!=None):
                newIndex.append(r)
                r+=1
            else:
                newIndex.append(0)
        
        self.n=r

        if self.n==1:
            return

        newCC=[]

        self.conexions=[]

        for i in range(self.n):
            self.conexions.append([])
            newCC.append([])

        for i in range(len(self.bridges)):

            len0 = len(self.CC[self.cc[self.bridges[i][0]]])
            

            if(len0!=0):
                for j in range(len0):
                    newCC[newIndex[self.cc[self.bridges[i][0]]]].append(self.CC[self.cc[self.bridges[i][0]]][j])
                self.CC[self.cc[self.bridges[i][0]]]=[]
            
            len1 = len(self.CC[self.cc[self.bridges[i][1]]])
            
            if(len1!=0):
                for j in range(len1):
                    newCC[newIndex[self.cc[self.bridges[i][1]]]].append(self.CC[self.cc[self.bridges[i][1]]][j])
                self.CC[self.cc[self.bridges[i][1]]]=[]
            
            self.conexions[newIndex[self.cc[self.bridges[i][0]]]].append((newIndex[self.cc[self.bridges[i][1]]],True))
            self.conexions[newIndex[self.cc[self.bridges[i][1]]]].append((newIndex[self.cc[self.bridges[i][0]]],True))

        self.CC= newCC

        for i in range(len(self.cc)):
            self.cc[i]=newIndex[self.cc[i]]





            





if __name__ == '__main__':
    main()