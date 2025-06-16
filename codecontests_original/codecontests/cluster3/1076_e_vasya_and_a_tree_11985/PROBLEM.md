# 1076_E. Vasya and a Tree

**ID:** 1076_e_vasya_and_a_tree_11985
**Difficulty:** 11

## Description

Vasya has a tree consisting of n vertices with root in vertex 1. At first all vertices has 0 written on it.

Let d(i, j) be the distance between vertices i and j, i.e. number of edges in the shortest path from i to j. Also, let's denote k-subtree of vertex x — set of vertices y such that next two conditions are met: 

  * x is the ancestor of y (each vertex is the ancestor of itself); 
  * d(x, y) ≤ k. 



Vasya needs you to process m queries. The i-th query is a triple v_i, d_i and x_i. For each query Vasya adds value x_i to each vertex from d_i-subtree of v_i.

Report to Vasya all values, written on vertices of the tree after processing all queries.

Input

The first line contains single integer n (1 ≤ n ≤ 3 ⋅ 10^5) — number of vertices in the tree.

Each of next n - 1 lines contains two integers x and y (1 ≤ x, y ≤ n) — edge between vertices x and y. It is guarantied that given graph is a tree.

Next line contains single integer m (1 ≤ m ≤ 3 ⋅ 10^5) — number of queries.

Each of next m lines contains three integers v_i, d_i, x_i (1 ≤ v_i ≤ n, 0 ≤ d_i ≤ 10^9, 1 ≤ x_i ≤ 10^9) — description of the i-th query.

Output

Print n integers. The i-th integers is the value, written in the i-th vertex after processing all queries.

Examples

Input


5
1 2
1 3
2 4
2 5
3
1 1 1
2 0 10
4 10 100


Output


1 11 1 100 0 


Input


5
2 3
2 1
5 4
3 4
5
2 0 4
3 10 1
1 2 3
2 3 10
1 1 7


Output


10 24 14 11 11 

Note

In the first exapmle initial values in vertices are 0, 0, 0, 0, 0. After the first query values will be equal to 1, 1, 1, 0, 0. After the second query values will be equal to 1, 11, 1, 0, 0. After the third query values will be equal to 1, 11, 1, 100, 0.

## Categories

- data structures
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5
1 2
1 3
2 4
2 5
3
1 1 1
2 0 10
4 10 100
```

**Output**:
```
1 11 1 100 0
```

### Example 2

**Input**:
```
5
2 3
2 1
5 4
3 4
5
2 0 4
3 10 1
1 2 3
2 3 10
1 1 7
```

**Output**:
```
10 24 14 11 11
```

### Example 3

**Input**:
```
1
3
1 1000000000 1000000000
1 1000000000 1000000000
1 1000000000 1000000000
```

**Output**:
```
3000000000
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
