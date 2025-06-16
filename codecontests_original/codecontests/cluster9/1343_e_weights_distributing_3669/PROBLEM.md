# 1343_E. Weights Distributing

**ID:** 1343_e_weights_distributing_3669
**Difficulty:** 11

## Description

You are given an undirected unweighted graph consisting of n vertices and m edges (which represents the map of Bertown) and the array of prices p of length m. It is guaranteed that there is a path between each pair of vertices (districts).

Mike has planned a trip from the vertex (district) a to the vertex (district) b and then from the vertex (district) b to the vertex (district) c. He can visit the same district twice or more. But there is one issue: authorities of the city want to set a price for using the road so if someone goes along the road then he should pay the price corresponding to this road (he pays each time he goes along the road). The list of prices that will be used p is ready and they just want to distribute it between all roads in the town in such a way that each price from the array corresponds to exactly one road.

You are a good friend of Mike (and suddenly a mayor of Bertown) and want to help him to make his trip as cheap as possible. So, your task is to distribute prices between roads in such a way that if Mike chooses the optimal path then the price of the trip is the minimum possible. Note that you cannot rearrange prices after the start of the trip.

You have to answer t independent test cases.

Input

The first line of the input contains one integer t (1 ≤ t ≤ 10^4) — the number of test cases. Then t test cases follow.

The first line of the test case contains five integers n, m, a, b and c (2 ≤ n ≤ 2 ⋅ 10^5, n-1 ≤ m ≤ min((n(n-1))/(2), 2 ⋅ 10^5), 1 ≤ a, b, c ≤ n) — the number of vertices, the number of edges and districts in Mike's trip.

The second line of the test case contains m integers p_1, p_2, ..., p_m (1 ≤ p_i ≤ 10^9), where p_i is the i-th price from the array.

The following m lines of the test case denote edges: edge i is represented by a pair of integers v_i, u_i (1 ≤ v_i, u_i ≤ n, u_i ≠ v_i), which are the indices of vertices connected by the edge. There are no loops or multiple edges in the given graph, i. e. for each pair (v_i, u_i) there are no other pairs (v_i, u_i) or (u_i, v_i) in the array of edges, and for each pair (v_i, u_i) the condition v_i ≠ u_i is satisfied. It is guaranteed that the given graph is connected.

It is guaranteed that the sum of n (as well as the sum of m) does not exceed 2 ⋅ 10^5 (∑ n ≤ 2 ⋅ 10^5, ∑ m ≤ 2 ⋅ 10^5).

Output

For each test case, print the answer — the minimum possible price of Mike's trip if you distribute prices between edges optimally.

Example

Input


2
4 3 2 3 4
1 2 3
1 2
1 3
1 4
7 9 1 5 7
2 10 4 8 5 6 7 3 3
1 2
1 3
1 4
3 2
3 5
4 2
5 6
1 7
6 7


Output


7
12

Note

One of the possible solution to the first test case of the example:

<image>

One of the possible solution to the second test case of the example:

<image>

## Categories

- brute force
- graphs
- greedy
- shortest paths
- sortings

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2
4 3 2 3 4
1 2 3
1 2
1 3
1 4
7 9 1 5 7
2 10 4 8 5 6 7 3 3
1 2
1 3
1 4
3 2
3 5
4 2
5 6
1 7
6 7
```

**Output**:
```
7
12
```

### Example 2

**Input**:
```
2
4 3 2 3 4
1 2 3
1 2
1 3
1 4
7 9 1 5 7
2 10 4 8 5 6 7 3 3
1 2
1 3
1 4
3 2
3 5
4 2
5 6
1 4
6 7
```

**Output**:
```
7
12
```

### Example 3

**Input**:
```
2
4 3 2 3 4
2 2 3
1 2
1 3
1 4
7 9 1 5 7
2 10 4 8 5 6 7 3 3
1 2
1 3
1 4
3 2
3 5
4 2
5 6
1 4
6 7
```

**Output**:
```
9
12
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
