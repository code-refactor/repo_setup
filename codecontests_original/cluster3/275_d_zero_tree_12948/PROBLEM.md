# 275_D. Zero Tree

**ID:** 275_d_zero_tree_12948
**Difficulty:** 10

## Description

A tree is a graph with n vertices and exactly n - 1 edges; this graph should meet the following condition: there exists exactly one shortest (by number of edges) path between any pair of its vertices.

A subtree of a tree T is a tree with both vertices and edges as subsets of vertices and edges of T.

You're given a tree with n vertices. Consider its vertices numbered with integers from 1 to n. Additionally an integer is written on every vertex of this tree. Initially the integer written on the i-th vertex is equal to vi. In one move you can apply the following operation:

  1. Select the subtree of the given tree that includes the vertex with number 1. 
  2. Increase (or decrease) by one all the integers which are written on the vertices of that subtree. 



Calculate the minimum number of moves that is required to make all the integers written on the vertices of the given tree equal to zero.

Input

The first line of the input contains n (1 ≤ n ≤ 105). Each of the next n - 1 lines contains two integers ai and bi (1 ≤ ai, bi ≤ n; ai ≠ bi) indicating there's an edge between vertices ai and bi. It's guaranteed that the input graph is a tree. 

The last line of the input contains a list of n space-separated integers v1, v2, ..., vn (|vi| ≤ 109).

Output

Print the minimum number of operations needed to solve the task.

Please, do not write the %lld specifier to read or write 64-bit integers in С++. It is preferred to use the cin, cout streams or the %I64d specifier.

Examples

Input

3
1 2
1 3
1 -1 1


Output

3

## Categories

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
3
1 2
1 3
1 -1 1
```

**Output**:
```
3
```

### Example 2

**Input**:
```
5
2 3
4 5
2 5
1 3
0 2 1 4 3
```

**Output**:
```
8
```

### Example 3

**Input**:
```
5
3 1
2 4
3 4
2 5
0 -3 -1 2 4
```

**Output**:
```
20
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
