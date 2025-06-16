# 981_C. Useful Decomposition

**ID:** 981_c_useful_decomposition_4026
**Difficulty:** 9

## Description

Ramesses knows a lot about problems involving trees (undirected connected graphs without cycles)!

He created a new useful tree decomposition, but he does not know how to construct it, so he asked you for help!

The decomposition is the splitting the edges of the tree in some simple paths in such a way that each two paths have at least one common vertex. Each edge of the tree should be in exactly one path.

Help Remesses, find such a decomposition of the tree or derermine that there is no such decomposition.

Input

The first line contains a single integer n (2 ≤ n ≤ 10^{5}) the number of nodes in the tree.

Each of the next n - 1 lines contains two integers a_i and b_i (1 ≤ a_i, b_i ≤ n, a_i ≠ b_i) — the edges of the tree. It is guaranteed that the given edges form a tree.

Output

If there are no decompositions, print the only line containing "No".

Otherwise in the first line print "Yes", and in the second line print the number of paths in the decomposition m. 

Each of the next m lines should contain two integers u_i, v_i (1 ≤ u_i, v_i ≤ n, u_i ≠ v_i) denoting that one of the paths in the decomposition is the simple path between nodes u_i and v_i. 

Each pair of paths in the decomposition should have at least one common vertex, and each edge of the tree should be presented in exactly one path. You can print the paths and the ends of each path in arbitrary order.

If there are multiple decompositions, print any.

Examples

Input

4
1 2
2 3
3 4


Output

Yes
1
1 4


Input

6
1 2
2 3
3 4
2 5
3 6


Output

No


Input

5
1 2
1 3
1 4
1 5


Output

Yes
4
1 2
1 3
1 4
1 5

Note

The tree from the first example is shown on the picture below: <image> The number next to each edge corresponds to the path number in the decomposition. It is easy to see that this decomposition suits the required conditions.

The tree from the second example is shown on the picture below: <image> We can show that there are no valid decompositions of this tree.

The tree from the third example is shown on the picture below: <image> The number next to each edge corresponds to the path number in the decomposition. It is easy to see that this decomposition suits the required conditions.

## Categories

- implementation
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
6
1 2
2 3
3 4
2 5
3 6
```

**Output**:
```
No
```

### Example 2

**Input**:
```
4
1 2
2 3
3 4
```

**Output**:
```
Yes
1
1 4
```

### Example 3

**Input**:
```
5
1 2
1 3
1 4
1 5
```

**Output**:
```
Yes
4
1 2
1 3
1 4
1 5
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
