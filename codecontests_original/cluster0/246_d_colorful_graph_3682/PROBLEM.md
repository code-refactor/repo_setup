# 246_D. Colorful Graph

**ID:** 246_d_colorful_graph_3682
**Difficulty:** 10

## Description

You've got an undirected graph, consisting of n vertices and m edges. We will consider the graph's vertices numbered with integers from 1 to n. Each vertex of the graph has a color. The color of the i-th vertex is an integer ci.

Let's consider all vertices of the graph, that are painted some color k. Let's denote a set of such as V(k). Let's denote the value of the neighbouring color diversity for color k as the cardinality of the set Q(k) = {cu : cu ≠ k and there is vertex v belonging to set V(k) such that nodes v and u are connected by an edge of the graph}.

Your task is to find such color k, which makes the cardinality of set Q(k) maximum. In other words, you want to find the color that has the most diverse neighbours. Please note, that you want to find such color k, that the graph has at least one vertex with such color.

Input

The first line contains two space-separated integers n, m (1 ≤ n, m ≤ 105) — the number of vertices end edges of the graph, correspondingly. The second line contains a sequence of integers c1, c2, ..., cn (1 ≤ ci ≤ 105) — the colors of the graph vertices. The numbers on the line are separated by spaces.

Next m lines contain the description of the edges: the i-th line contains two space-separated integers ai, bi (1 ≤ ai, bi ≤ n; ai ≠ bi) — the numbers of the vertices, connected by the i-th edge. 

It is guaranteed that the given graph has no self-loops or multiple edges.

Output

Print the number of the color which has the set of neighbours with the maximum cardinality. It there are multiple optimal colors, print the color with the minimum number. Please note, that you want to find such color, that the graph has at least one vertex with such color.

Examples

Input

6 6
1 1 2 3 5 8
1 2
3 2
1 4
4 3
4 5
4 6


Output

3


Input

5 6
4 2 5 2 4
1 2
2 3
3 1
5 3
5 4
3 4


Output

2

## Categories

- brute force
- dfs and similar
- graphs

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5 6
4 2 5 2 4
1 2
2 3
3 1
5 3
5 4
3 4
```

**Output**:
```
2
```

### Example 2

**Input**:
```
6 6
1 1 2 3 5 8
1 2
3 2
1 4
4 3
4 5
4 6
```

**Output**:
```
3
```

### Example 3

**Input**:
```
10 15
1 1 1 1 2 2 2 2 1 2
8 5
9 1
8 6
3 5
2 7
2 9
10 3
3 2
3 6
4 2
5 9
7 3
6 7
5 10
4 7
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
