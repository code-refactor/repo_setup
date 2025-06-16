# 963_B. Destruction of a Tree

**ID:** 963_b_destruction_of_a_tree_65
**Difficulty:** 8

## Description

You are given a tree (a graph with n vertices and n - 1 edges in which it's possible to reach any vertex from any other vertex using only its edges).

A vertex can be destroyed if this vertex has even degree. If you destroy a vertex, all edges connected to it are also deleted.

Destroy all vertices in the given tree or determine that it is impossible.

Input

The first line contains integer n (1 ≤ n ≤ 2·105) — number of vertices in a tree.

The second line contains n integers p1, p2, ..., pn (0 ≤ pi ≤ n). If pi ≠ 0 there is an edge between vertices i and pi. It is guaranteed that the given graph is a tree.

Output

If it's possible to destroy all vertices, print "YES" (without quotes), otherwise print "NO" (without quotes).

If it's possible to destroy all vertices, in the next n lines print the indices of the vertices in order you destroy them. If there are multiple correct answers, print any.

Examples

Input

5
0 1 2 1 2


Output

YES
1
2
3
5
4


Input

4
0 1 2 3


Output

NO

Note

In the first example at first you have to remove the vertex with index 1 (after that, the edges (1, 2) and (1, 4) are removed), then the vertex with index 2 (and edges (2, 3) and (2, 5) are removed). After that there are no edges in the tree, so you can remove remaining vertices in any order.

<image>

## Categories

- constructive algorithms
- dfs and similar
- dp
- greedy
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5
0 1 2 1 2
```

**Output**:
```
YES
1
2
3
5
4
```

### Example 2

**Input**:
```
4
0 1 2 3
```

**Output**:
```
NO
```

### Example 3

**Input**:
```
21
11 19 4 19 6 0 13 7 6 2 5 3 16 10 1 9 15 21 9 21 2
```

**Output**:
```
YES
11
6
16
7
8
13
10
14
2
21
18
20
19
3
12
4
9
5
15
17
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
