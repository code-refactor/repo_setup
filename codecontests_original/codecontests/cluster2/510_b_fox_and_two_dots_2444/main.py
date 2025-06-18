#!/usr/bin/env python3

'''
Zijian He
1429876
'''
# Import
from sys import setrecursionlimit
setrecursionlimit(10**6)


# Function from class
class Graph:
    def __init__ (self):
        self._alist = {}

    def add_vertex (self, vertex):
        if vertex not in self._alist:
            self._alist[vertex] = set()

    def add_edge (self, source, destination):
        self.add_vertex(source)
        self.add_vertex(destination)
        self._alist[source].add(destination)

    def is_edge (self, source, destination):
        return (self.is_vertex(source)
                and destination in self._alist[source])

    def is_vertex (self, vertex):
        return vertex in self._alist

    def neighbours (self, vertex):
        return self._alist[vertex]

    def vertices (self):
        return self._alist.keys()

class UndirectedGraph (Graph):
    def add_edge (self, a, b):
        super().add_edge (a, b)
        super().add_edge (b, a)

def depth_first_search(g, v):
    reached = {}
    def do_dfs(curr, prev):
        if curr in reached:
            return
        reached[curr] = prev
        for succ in g.neighbours(curr):
            do_dfs(succ, curr)
    do_dfs(v, v)
    return reached
#-----------------------------------------------------------------------

# Declaire the variables for checking the cycle
Detect = False

vertex = {}

def dfs_v2(g, curr, prev):
	global Detect
	global vertex
	
	if Detect:
		return
		
	vertex[curr] = True

	for succ in g.neighbours(curr):
	
		if vertex[succ] and succ != prev:
			Detect = True
			return
		if not vertex[succ]:
			dfs_v2(g, succ, curr)


def cycle(g):
	global Detect
	global vertex
	
	# Initialize all the node as unmarked
	for i in g.vertices():
		vertex[i] = False
		
	# Check throughout the node
	for j in g.vertices():
		if not vertex[j]:
			dfs_v2(g, j, j)
		if Detect:
			break
	return 

# ----------------------------------------------------------------------



# Process the input
row, col = map(int, input().split(" "))
rows = []

for i in range(row):
	rows.append(input())
	
# Set node as a dictionary
node = {}

for i in range(row):
	for j in range(col):
		node[i * col + j] = rows[i][j]
	
# Set up the graph
result_Graph = UndirectedGraph()

# Connecting the node with same color
for i in range(row * col):
	
	result_Graph.add_vertex(i)
	
	try:
		if node[i] == node[i + 1] and (i % col) != (col - 1):
			result_Graph.add_edge(i, i + 1)	
			
		if node[i] == node[i + col]:
			result_Graph.add_edge(i, i + col)
	except:
		continue

# Main function
cycle(result_Graph)

if Detect:
	print("Yes")
	
else:
	print("No")
