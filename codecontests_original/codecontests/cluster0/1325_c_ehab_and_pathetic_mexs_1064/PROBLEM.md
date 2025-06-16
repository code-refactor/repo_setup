# 1325_C. Ehab and Path-etic MEXs

**ID:** 1325_c_ehab_and_pathetic_mexs_1064
**Difficulty:** 9

## Description

You are given a tree consisting of n nodes. You want to write some labels on the tree's edges such that the following conditions hold:

  * Every label is an integer between 0 and n-2 inclusive. 
  * All the written labels are distinct. 
  * The largest value among MEX(u,v) over all pairs of nodes (u,v) is as small as possible. 



Here, MEX(u,v) denotes the smallest non-negative integer that isn't written on any edge on the unique simple path from node u to node v.

Input

The first line contains the integer n (2 ≤ n ≤ 10^5) — the number of nodes in the tree.

Each of the next n-1 lines contains two space-separated integers u and v (1 ≤ u,v ≤ n) that mean there's an edge between nodes u and v. It's guaranteed that the given graph is a tree.

Output

Output n-1 integers. The i^{th} of them will be the number written on the i^{th} edge (in the input order).

Examples

Input


3
1 2
1 3


Output


0
1


Input


6
1 2
1 3
2 4
2 5
5 6


Output


0
3
2
4
1

Note

The tree from the second sample:

<image>

## Categories

- constructive algorithms
- dfs and similar
- greedy
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
6
1 2
1 3
2 4
2 5
5 6
```

**Output**:
```
0
3
1
2
4
```

### Example 2

**Input**:
```
3
1 2
1 3
```

**Output**:
```
0
1
```

### Example 3

**Input**:
```
6
1 2
2 3
3 4
3 5
3 6
```

**Output**:
```
0
4
1
2
3
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
