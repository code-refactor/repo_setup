# 1041_E. Tree Reconstruction

**ID:** 1041_e_tree_reconstruction_8858
**Difficulty:** 11

## Description

Monocarp has drawn a tree (an undirected connected acyclic graph) and then has given each vertex an index. All indices are distinct numbers from 1 to n. For every edge e of this tree, Monocarp has written two numbers: the maximum indices of the vertices of the two components formed if the edge e (and only this edge) is erased from the tree.

Monocarp has given you a list of n - 1 pairs of numbers. He wants you to provide an example of a tree that will produce the said list if this tree exists. If such tree does not exist, say so.

Input

The first line contains one integer n (2 ≤ n ≤ 1 000) — the number of vertices in the tree.

Each of the next n-1 lines contains two integers a_i and b_i each (1 ≤ a_i < b_i ≤ n) — the maximal indices of vertices in the components formed if the i-th edge is removed.

Output

If there is no such tree that can produce the given list of pairs, print "NO" (without quotes).

Otherwise print "YES" (without quotes) in the first line and the edges of the tree in the next n - 1 lines. Each of the last n - 1 lines should contain two integers x_i and y_i (1 ≤ x_i, y_i ≤ n) — vertices connected by an edge.

Note: The numeration of edges doesn't matter for this task. Your solution will be considered correct if your tree produces the same pairs as given in the input file (possibly reordered). That means that you can print the edges of the tree you reconstructed in any order.

Examples

Input

4
3 4
1 4
3 4


Output

YES
1 3
3 2
2 4


Input

3
1 3
1 3


Output

NO


Input

3
1 2
2 3


Output

NO

Note

Possible tree from the first example. Dotted lines show edges you need to remove to get appropriate pairs. 

<image>

## Categories

- constructive algorithms
- data structures
- graphs
- greedy

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
1 2
2 3
```

**Output**:
```
NO
```

### Example 2

**Input**:
```
4
3 4
1 4
3 4
```

**Output**:
```
YES
1 3
3 2
2 4
```

### Example 3

**Input**:
```
3
1 3
1 3
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
