# 1133_F1. Spanning Tree with Maximum Degree

**ID:** 1133_f1_spanning_tree_with_maximum_degree_10945
**Difficulty:** 12

## Description

You are given an undirected unweighted connected graph consisting of n vertices and m edges. It is guaranteed that there are no self-loops or multiple edges in the given graph.

Your task is to find any spanning tree of this graph such that the maximum degree over all vertices is maximum possible. Recall that the degree of a vertex is the number of edges incident to it.

Input

The first line contains two integers n and m (2 ≤ n ≤ 2 ⋅ 10^5, n - 1 ≤ m ≤ min(2 ⋅ 10^5, (n(n-1))/(2))) — the number of vertices and edges, respectively.

The following m lines denote edges: edge i is represented by a pair of integers v_i, u_i (1 ≤ v_i, u_i ≤ n, u_i ≠ v_i), which are the indices of vertices connected by the edge. There are no loops or multiple edges in the given graph, i. e. for each pair (v_i, u_i) there are no other pairs (v_i, u_i) or (u_i, v_i) in the list of edges, and for each pair (v_i, u_i) the condition v_i ≠ u_i is satisfied.

Output

Print n-1 lines describing the edges of a spanning tree such that the maximum degree over all vertices is maximum possible. Make sure that the edges of the printed spanning tree form some subset of the input edges (order doesn't matter and edge (v, u) is considered the same as the edge (u, v)).

If there are multiple possible answers, print any of them.

Examples

Input


5 5
1 2
2 3
3 5
4 3
1 5


Output


3 5
2 1
3 2
3 4


Input


4 6
1 2
1 3
1 4
2 3
2 4
3 4


Output


4 1
1 2
1 3


Input


8 9
1 2
2 3
2 5
1 6
3 4
6 5
4 5
2 7
5 8


Output


3 2
2 5
8 5
6 1
2 7
1 2
3 4

Note

Picture corresponding to the first example: <image>

In this example the number of edges of spanning tree incident to the vertex 3 is 3. It is the maximum degree over all vertices of the spanning tree. It is easy to see that we cannot obtain a better answer.

Picture corresponding to the second example: <image>

In this example the number of edges of spanning tree incident to the vertex 1 is 3. It is the maximum degree over all vertices of the spanning tree. It is easy to see that we cannot obtain a better answer.

Picture corresponding to the third example: <image>

In this example the number of edges of spanning tree incident to the vertex 2 is 4. It is the maximum degree over all vertices of the spanning tree. It is easy to see that we cannot obtain a better answer. But because this example is symmetric, we can choose almost the same spanning tree but with vertex 5 instead of 2.

## Categories

- graphs

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4 6
1 2
1 3
1 4
2 3
2 4
3 4
```

**Output**:
```
1 2
1 3
1 4
```

### Example 2

**Input**:
```
8 9
1 2
2 3
2 5
1 6
3 4
6 5
4 5
2 7
5 8
```

**Output**:
```
2 1
2 3
2 5
2 7
1 6
3 4
5 8
```

### Example 3

**Input**:
```
5 5
1 2
2 3
3 5
4 3
1 5
```

**Output**:
```
3 2
3 5
3 4
2 1
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
