# 1086_B. Minimum Diameter Tree

**ID:** 1086_b_minimum_diameter_tree_8860
**Difficulty:** 8

## Description

You are given a tree (an undirected connected graph without cycles) and an integer s.

Vanya wants to put weights on all edges of the tree so that all weights are non-negative real numbers and their sum is s. At the same time, he wants to make the diameter of the tree as small as possible.

Let's define the diameter of a weighed tree as the maximum sum of the weights of the edges lying on the path between two some vertices of the tree. In other words, the diameter of a weighed tree is the length of the longest simple path in the tree, where length of a path is equal to the sum of weights over all edges in the path.

Find the minimum possible diameter that Vanya can get.

Input

The first line contains two integer numbers n and s (2 ≤ n ≤ 10^5, 1 ≤ s ≤ 10^9) — the number of vertices in the tree and the sum of edge weights.

Each of the following n−1 lines contains two space-separated integer numbers a_i and b_i (1 ≤ a_i, b_i ≤ n, a_i ≠ b_i) — the indexes of vertices connected by an edge. The edges are undirected.

It is guaranteed that the given edges form a tree.

Output

Print the minimum diameter of the tree that Vanya can get by placing some non-negative real weights on its edges with the sum equal to s.

Your answer will be considered correct if its absolute or relative error does not exceed 10^{-6}.

Formally, let your answer be a, and the jury's answer be b. Your answer is considered correct if \frac {|a-b|} {max(1, b)} ≤ 10^{-6}.

Examples

Input


4 3
1 2
1 3
1 4


Output


2.000000000000000000

Input


6 1
2 1
2 3
2 5
5 4
5 6


Output


0.500000000000000000

Input


5 5
1 2
2 3
3 4
3 5


Output


3.333333333333333333

Note

In the first example it is necessary to put weights like this:

<image>

It is easy to see that the diameter of this tree is 2. It can be proved that it is the minimum possible diameter.

In the second example it is necessary to put weights like this:

<image>

## Categories

- constructive algorithms
- implementation
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
6 1
2 1
2 3
2 5
5 4
5 6
```

**Output**:
```
0.5000000000
```

### Example 2

**Input**:
```
4 3
1 2
1 3
1 4
```

**Output**:
```
2.0000000000
```

### Example 3

**Input**:
```
5 5
1 2
2 3
3 4
3 5
```

**Output**:
```
3.3333333333
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
