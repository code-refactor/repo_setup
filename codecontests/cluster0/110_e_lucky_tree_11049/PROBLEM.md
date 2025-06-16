# 110_E. Lucky Tree

**ID:** 110_e_lucky_tree_11049
**Difficulty:** 11

## Description

Petya loves lucky numbers. We all know that lucky numbers are the positive integers whose decimal representations contain only the lucky digits 4 and 7. For example, numbers 47, 744, 4 are lucky and 5, 17, 467 are not.

One day Petya encountered a tree with n vertexes. Besides, the tree was weighted, i. e. each edge of the tree has weight (a positive integer). An edge is lucky if its weight is a lucky number. Note that a tree with n vertexes is an undirected connected graph that has exactly n - 1 edges.

Petya wondered how many vertex triples (i, j, k) exists that on the way from i to j, as well as on the way from i to k there must be at least one lucky edge (all three vertexes are pairwise distinct). The order of numbers in the triple matters, that is, the triple (1, 2, 3) is not equal to the triple (2, 1, 3) and is not equal to the triple (1, 3, 2). 

Find how many such triples of vertexes exist.

Input

The first line contains the single integer n (1 ≤ n ≤ 105) — the number of tree vertexes. Next n - 1 lines contain three integers each: ui vi wi (1 ≤ ui, vi ≤ n, 1 ≤ wi ≤ 109) — the pair of vertexes connected by the edge and the edge's weight.

Output

On the single line print the single number — the answer.

Please do not use the %lld specificator to read or write 64-bit numbers in С++. It is recommended to use the cin, cout streams or the %I64d specificator.

Examples

Input

4
1 2 4
3 1 2
1 4 7


Output

16


Input

4
1 2 4
1 3 47
1 4 7447


Output

24

Note

The 16 triples of vertexes from the first sample are: (1, 2, 4), (1, 4, 2), (2, 1, 3), (2, 1, 4), (2, 3, 1), (2, 3, 4), (2, 4, 1), (2, 4, 3), (3, 2, 4), (3, 4, 2), (4, 1, 2), (4, 1, 3), (4, 2, 1), (4, 2, 3), (4, 3, 1), (4, 3, 2).

In the second sample all the triples should be counted: 4·3·2 = 24.

## Categories

- dp
- dsu
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4
1 2 4
1 3 47
1 4 7447
```

**Output**:
```
24
```

### Example 2

**Input**:
```
4
1 2 4
3 1 2
1 4 7
```

**Output**:
```
16
```

### Example 3

**Input**:
```
10
9 2 6
5 3 7
7 8 9
2 1 7
8 6 3
1 4 5
3 10 7
7 4 3
6 3 5
```

**Output**:
```
328
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
