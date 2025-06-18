# 1486_E. Paired Payment

**ID:** 1486_e_paired_payment_6798
**Difficulty:** 11

## Description

There are n cities and m bidirectional roads in the country. The roads in the country form an undirected weighted graph. The graph is not guaranteed to be connected. Each road has it's own parameter w. You can travel through the roads, but the government made a new law: you can only go through two roads at a time (go from city a to city b and then from city b to city c) and you will have to pay (w_{ab} + w_{bc})^2 money to go through those roads. Find out whether it is possible to travel from city 1 to every other city t and what's the minimum amount of money you need to get from 1 to t.

Input

First line contains two integers n, m (2 ≤ n ≤ 10^5, 1 ≤ m ≤ min((n ⋅ (n - 1))/(2), 2 ⋅ 10^5)).

Next m lines each contain three integers v_i, u_i, w_i (1 ≤ v_i, u_i ≤ n, 1 ≤ w_i ≤ 50, u_i ≠ v_i). It's guaranteed that there are no multiple edges, i.e. for any edge (u_i, v_i) there are no other edges (u_i, v_i) or (v_i, u_i).

Output

For every city t print one integer. If there is no correct path between 1 and t output -1. Otherwise print out the minimum amount of money needed to travel from 1 to t.

Examples

Input


5 6
1 2 3
2 3 4
3 4 5
4 5 6
1 5 1
2 4 2


Output


0 98 49 25 114 

Input


3 2
1 2 1
2 3 2


Output


0 -1 9 

Note

The graph in the first example looks like this.

<image>

In the second example the path from 1 to 3 goes through 2, so the resulting payment is (1 + 2)^2 = 9.

<image>

## Categories

- binary search
- brute force
- constructive algorithms
- dp
- flows
- graphs
- shortest paths

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3 2
1 2 1
2 3 2
```

**Output**:
```
0 -1 9
```

### Example 2

**Input**:
```
5 6
1 2 3
2 3 4
3 4 5
4 5 6
1 5 1
2 4 2
```

**Output**:
```
0 98 49 25 114
```

### Example 3

**Input**:
```
10 20
10 1 15
7 1 32
5 3 36
3 9 14
3 4 19
6 8 4
9 6 18
7 3 38
10 7 12
7 5 29
7 6 14
6 2 40
8 9 19
7 8 11
7 4 19
2 1 38
10 9 3
6 5 50
10 3 41
1 8 3
```

**Output**:
```
0 2201 779 1138 1898 49 196 520 324 490
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
