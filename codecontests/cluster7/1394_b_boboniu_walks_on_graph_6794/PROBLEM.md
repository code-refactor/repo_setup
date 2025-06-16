# 1394_B. Boboniu Walks on Graph

**ID:** 1394_b_boboniu_walks_on_graph_6794
**Difficulty:** 8

## Description

Boboniu has a directed graph with n vertices and m edges.

The out-degree of each vertex is at most k.

Each edge has an integer weight between 1 and m. No two edges have equal weights.

Boboniu likes to walk on the graph with some specific rules, which is represented by a tuple (c_1,c_2,…,c_k). If he now stands on a vertex u with out-degree i, then he will go to the next vertex by the edge with the c_i-th (1≤ c_i≤ i) smallest weight among all edges outgoing from u.

Now Boboniu asks you to calculate the number of tuples (c_1,c_2,…,c_k) such that

  * 1≤ c_i≤ i for all i (1≤ i≤ k). 
  * Starting from any vertex u, it is possible to go back to u in finite time by walking on the graph under the described rules. 

Input

The first line contains three integers n, m and k (2≤ n≤ 2⋅ 10^5, 2≤ m≤ min(2⋅ 10^5,n(n-1) ), 1≤ k≤ 9).

Each of the next m lines contains three integers u, v and w (1≤ u,v≤ n,u≠ v,1≤ w≤ m), denoting an edge from u to v with weight w. It is guaranteed that there are no self-loops or multiple edges and each vertex has at least one edge starting from itself.

It is guaranteed that the out-degree of each vertex is at most k and no two edges have equal weight.

Output

Print one integer: the number of tuples.

Examples

Input


4 6 3
4 2 1
1 2 2
2 4 3
4 1 4
4 3 5
3 1 6


Output


2


Input


5 5 1
1 4 1
5 1 2
2 5 3
4 3 4
3 2 5


Output


1


Input


6 13 4
3 5 1
2 5 2
6 3 3
1 4 4
2 6 5
5 3 6
4 1 7
4 3 8
5 2 9
4 2 10
2 1 11
6 1 12
4 6 13


Output


1

Note

For the first example, there are two tuples: (1,1,3) and (1,2,3). The blue edges in the picture denote the c_i-th smallest edges for each vertex, which Boboniu chooses to go through.

<image>

For the third example, there's only one tuple: (1,2,2,2).

<image>

The out-degree of vertex u means the number of edges outgoing from u.

## Categories

- brute force
- dfs and similar
- graphs
- hashing

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5 5 1
1 4 1
5 1 2
2 5 3
4 3 4
3 2 5
```

**Output**:
```
1
```

### Example 2

**Input**:
```
4 6 3
4 2 1
1 2 2
2 4 3
4 1 4
4 3 5
3 1 6
```

**Output**:
```
2
```

### Example 3

**Input**:
```
6 13 4
3 5 1
2 5 2
6 3 3
1 4 4
2 6 5
5 3 6
4 1 7
4 3 8
5 2 9
4 2 10
2 1 11
6 1 12
4 6 13
```

**Output**:
```
1
```


## Testing

Run the solution with:

```bash
./run.sh
```

Or test with a specific input file:

```bash
uv run main.py < tests/input_1.txt
```
