# 1176_E. Cover it!

**ID:** 1176_e_cover_it_10635
**Difficulty:** 11

## Description

You are given an undirected unweighted connected graph consisting of n vertices and m edges. It is guaranteed that there are no self-loops or multiple edges in the given graph.

Your task is to choose at most ⌊n/2⌋ vertices in this graph so each unchosen vertex is adjacent (in other words, connected by an edge) to at least one of chosen vertices.

It is guaranteed that the answer exists. If there are multiple answers, you can print any.

You will be given multiple independent queries to answer.

Input

The first line contains a single integer t (1 ≤ t ≤ 2 ⋅ 10^5) — the number of queries.

Then t queries follow.

The first line of each query contains two integers n and m (2 ≤ n ≤ 2 ⋅ 10^5, n - 1 ≤ m ≤ min(2 ⋅ 10^5, (n(n-1))/(2))) — the number of vertices and the number of edges, respectively.

The following m lines denote edges: edge i is represented by a pair of integers v_i, u_i (1 ≤ v_i, u_i ≤ n, u_i ≠ v_i), which are the indices of vertices connected by the edge.

There are no self-loops or multiple edges in the given graph, i. e. for each pair (v_i, u_i) there are no other pairs (v_i, u_i) or (u_i, v_i) in the list of edges, and for each pair (v_i, u_i) the condition v_i ≠ u_i is satisfied. It is guaranteed that the given graph is connected.

It is guaranteed that ∑ m ≤ 2 ⋅ 10^5 over all queries.

Output

For each query print two lines.

In the first line print k (1 ≤ ⌊n/2⌋) — the number of chosen vertices.

In the second line print k distinct integers c_1, c_2, ..., c_k in any order, where c_i is the index of the i-th chosen vertex.

It is guaranteed that the answer exists. If there are multiple answers, you can print any.

Example

Input


2
4 6
1 2
1 3
1 4
2 3
2 4
3 4
6 8
2 5
5 4
4 3
4 1
1 3
2 3
2 6
5 6


Output


2
1 3
3
4 3 6

Note

In the first query any vertex or any pair of vertices will suffice.

<image>

Note that you don't have to minimize the number of chosen vertices. In the second query two vertices can be enough (vertices 2 and 4) but three is also ok.

<image>

## Categories

- dfs and similar
- dsu
- graphs
- shortest paths
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2
4 6
1 2
1 3
1 4
2 3
2 4
3 4
6 8
2 5
5 4
4 3
4 1
1 3
2 3
2 6
5 6
```

**Output**:
```
1
1 
3
3 4 6
```

### Example 2

**Input**:
```
5 6
2 1
2 3
2 4
2 5
3 4
3 5
```

**Output**:
```
2 1
2 3
2 4
2 5
```

### Example 3

**Input**:
```
5 6
1 5
2 5
3 5
4 5
2 3
1 2
```

**Output**:
```
5 1
5 2
5 3
5 4
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
