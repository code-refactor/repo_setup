# 274_B. Zero Tree

**ID:** 274_b_zero_tree_3163
**Difficulty:** 8

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
12
1 6
10 1
4 1
7 1
1 2
5 1
1 8
1 11
3 1
12 1
9 1
580660007 861441526 -264928594 488291045 253254575 -974301934 709266786 926718320 87511873 514836444 -702876508 848928657
```

**Output**:
```
2529263875
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
