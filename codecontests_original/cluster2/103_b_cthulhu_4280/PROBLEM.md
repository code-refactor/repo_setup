# 103_B. Cthulhu

**ID:** 103_b_cthulhu_4280
**Difficulty:** 8

## Description

...Once upon a time a man came to the sea. The sea was stormy and dark. The man started to call for the little mermaid to appear but alas, he only woke up Cthulhu...

Whereas on the other end of the world Pentagon is actively collecting information trying to predict the monster's behavior and preparing the secret super weapon. Due to high seismic activity and poor weather conditions the satellites haven't yet been able to make clear shots of the monster. The analysis of the first shot resulted in an undirected graph with n vertices and m edges. Now the world's best minds are about to determine whether this graph can be regarded as Cthulhu or not.

To add simplicity, let's suppose that Cthulhu looks from the space like some spherical body with tentacles attached to it. Formally, we shall regard as Cthulhu such an undirected graph that can be represented as a set of three or more rooted trees, whose roots are connected by a simple cycle.

It is guaranteed that the graph contains no multiple edges and self-loops.

<image>

Input

The first line contains two integers — the number of vertices n and the number of edges m of the graph (1 ≤ n ≤ 100, 0 ≤ m ≤ <image>).

Each of the following m lines contains a pair of integers x and y, that show that an edge exists between vertices x and y (1 ≤ x, y ≤ n, x ≠ y). For each pair of vertices there will be at most one edge between them, no edge connects a vertex to itself.

Output

Print "NO", if the graph is not Cthulhu and "FHTAGN!" if it is.

Examples

Input

6 6
6 3
6 4
5 1
2 5
1 4
5 4


Output

FHTAGN!

Input

6 5
5 6
4 6
3 1
5 1
1 2


Output

NO

Note

Let us denote as a simple cycle a set of v vertices that can be numbered so that the edges will only exist between vertices number 1 and 2, 2 and 3, ..., v - 1 and v, v and 1.

A tree is a connected undirected graph consisting of n vertices and n - 1 edges (n > 0).

A rooted tree is a tree where one vertex is selected to be the root.

## Categories

- dfs and similar
- dsu
- graphs

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
6 5
5 6
4 6
3 1
5 1
1 2
```

**Output**:
```
NO
```

### Example 2

**Input**:
```
6 6
6 3
6 4
5 1
2 5
1 4
5 4
```

**Output**:
```
FHTAGN!
```

### Example 3

**Input**:
```
100 66
41 14
19 13
70 43
79 62
9 62
71 40
53 86
80 4
34 33
72 68
40 96
84 59
36 77
55 50
40 3
79 81
3 43
33 47
22 98
33 90
56 49
69 28
73 30
65 22
98 20
9 52
54 20
32 70
51 80
63 12
21 48
35 17
48 87
25 43
65 80
42 3
86 35
95 98
43 59
51 46
66 37
88 34
32 47
24 42
21 44
92 59
81 6
100 82
85 6
58 25
66 6
14 32
59 85
3 98
44 4
85 51
69 41
80 70
81 24
75 71
93 9
82 55
70 46
66 32
77 58
11 46
```

**Output**:
```
NO
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
