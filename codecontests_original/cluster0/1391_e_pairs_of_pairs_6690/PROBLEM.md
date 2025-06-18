# 1391_E. Pairs of Pairs

**ID:** 1391_e_pairs_of_pairs_6690
**Difficulty:** 11

## Description

You have a simple and connected undirected graph consisting of n nodes and m edges.

Consider any way to pair some subset of these n nodes such that no node is present in more than one pair. 

This pairing is valid if for every pair of pairs, the induced subgraph containing all 4 nodes, two from each pair, has at most 2 edges (out of the 6 possible edges). More formally, for any two pairs, (a,b) and (c,d), the induced subgraph with nodes \\{a,b,c,d\} should have at most 2 edges. 

Please note that the subgraph induced by a set of nodes contains nodes only from this set and edges which have both of its end points in this set.

Now, do one of the following: 

  * Find a simple path consisting of at least ⌈ n/2 ⌉ nodes. Here, a path is called simple if it does not visit any node multiple times. 
  * Find a valid pairing in which at least ⌈ n/2 ⌉ nodes are paired. 



It can be shown that it is possible to find at least one of the two in every graph satisfying constraints from the statement. 

Input

Each test contains multiple test cases. The first line contains the number of test cases t (1 ≤ t ≤ 10^5). Description of the test cases follows.

The first line of each test case contains 2 integers n, m (2 ≤ n ≤ 5⋅ 10^5, 1 ≤ m ≤ 10^6), denoting the number of nodes and edges, respectively. 

The next m lines each contain 2 integers u and v (1 ≤ u, v ≤ n, u ≠ v), denoting that there is an undirected edge between nodes u and v in the given graph.

It is guaranteed that the given graph is connected, and simple — it does not contain multiple edges between the same pair of nodes, nor does it have any self-loops. 

It is guaranteed that the sum of n over all test cases does not exceed 5⋅ 10^5.

It is guaranteed that the sum of m over all test cases does not exceed 10^6.

Output

For each test case, the output format is as follows. 

If you have found a pairing, in the first line output "PAIRING" (without quotes). 

  * Then, output k (⌈ n/2 ⌉ ≤ 2⋅ k ≤ n), the number of pairs in your pairing. 
  * Then, in each of the next k lines, output 2 integers a and b — denoting that a and b are paired with each other. Note that the graph does not have to have an edge between a and b!
  * This pairing has to be valid, and every node has to be a part of at most 1 pair. 



Otherwise, in the first line output "PATH" (without quotes). 

  * Then, output k (⌈ n/2 ⌉ ≤ k ≤ n), the number of nodes in your path. 
  * Then, in the second line, output k integers, v_1, v_2, …, v_k, in the order in which they appear on the path. Formally, v_i and v_{i+1} should have an edge between them for every i (1 ≤ i < k).
  * This path has to be simple, meaning no node should appear more than once. 

Example

Input


4
6 5
1 4
2 5
3 6
1 5
3 5
6 5
1 4
2 5
3 6
1 5
3 5
12 14
1 2
2 3
3 4
4 1
1 5
1 12
2 6
2 7
3 8
3 9
4 10
4 11
2 4
1 3
12 14
1 2
2 3
3 4
4 1
1 5
1 12
2 6
2 7
3 8
3 9
4 10
4 11
2 4
1 3


Output


PATH
4 
1 5 3 6
PAIRING
2
1 6
2 4
PAIRING
3
1 8
2 5
4 10
PAIRING
4
1 7
2 9
3 11
4 5

Note

The path outputted in the first case is the following. 

<image>

The pairing outputted in the second case is the following. 

<image>

Here is an invalid pairing for the same graph — the subgraph \{1,3,4,5\} has 3 edges. 

<image>

Here is the pairing outputted in the third case. 

<image>

It's valid because — 

  * The subgraph \{1,8,2,5\} has edges (1,2) and (1,5). 
  * The subgraph \{1,8,4,10\} has edges (1,4) and (4,10). 
  * The subgraph \{4,10,2,5\} has edges (2,4) and (4,10). 



Here is the pairing outputted in the fourth case. 

<image>

## Categories

- constructive algorithms
- dfs and similar
- graphs
- greedy
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4
6 5
1 4
2 5
3 6
1 5
3 5
6 5
1 4
2 5
3 6
1 5
3 5
12 14
1 2
2 3
3 4
4 1
1 5
1 12
2 6
2 7
3 8
3 9
4 10
4 11
2 4
1 3
12 14
1 2
2 3
3 4
4 1
1 5
1 12
2 6
2 7
3 8
3 9
4 10
4 11
2 4
1 3
```

**Output**:
```
PATH
3
2 5 1 
PATH
3
2 5 1 
PAIRING
4
2 5
3 6
4 8
10 11
PAIRING
4
2 5
3 6
4 8
10 11
```

### Example 2

**Input**:
```
1
20 37
17 10
6 10
20 14
4 7
3 16
5 11
16 17
17 6
10 5
10 2
12 9
11 18
11 12
9 1
12 18
18 1
2 5
19 12
4 8
8 7
5 19
8 20
2 19
1 4
18 9
20 15
7 14
19 11
14 15
13 16
3 13
9 4
1 8
6 2
16 6
13 17
7 20
```

**Output**:
```
PATH
11
19 2 6 16 17 10 5 11 12 9 1
```

### Example 3

**Input**:
```
4
6 5
1 4
2 5
3 6
1 5
3 5
6 5
1 4
2 5
3 6
1 5
3 5
12 14
1 2
2 3
3 4
4 1
1 5
1 12
2 6
2 7
3 8
3 9
4 10
4 11
2 4
1 3
12 14
1 2
2 3
3 4
4 1
1 5
1 12
2 6
2 7
3 8
3 9
4 10
4 11
2 4
1 3
```

**Output**:
```
PATH
3
2 5 1 
PATH
3
2 5 1 
PAIRING
4
2 5
3 6
4 8
10 11
PAIRING
4
2 5
3 6
4 8
10 11
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
