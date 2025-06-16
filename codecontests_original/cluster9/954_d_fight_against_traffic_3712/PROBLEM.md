# 954_D. Fight Against Traffic

**ID:** 954_d_fight_against_traffic_3712
**Difficulty:** 10

## Description

Little town Nsk consists of n junctions connected by m bidirectional roads. Each road connects two distinct junctions and no two roads connect the same pair of junctions. It is possible to get from any junction to any other junction by these roads. The distance between two junctions is equal to the minimum possible number of roads on a path between them.

In order to improve the transportation system, the city council asks mayor to build one new road. The problem is that the mayor has just bought a wonderful new car and he really enjoys a ride from his home, located near junction s to work located near junction t. Thus, he wants to build a new road in such a way that the distance between these two junctions won't decrease. 

You are assigned a task to compute the number of pairs of junctions that are not connected by the road, such that if the new road between these two junctions is built the distance between s and t won't decrease.

Input

The firt line of the input contains integers n, m, s and t (2 ≤ n ≤ 1000, 1 ≤ m ≤ 1000, 1 ≤ s, t ≤ n, s ≠ t) — the number of junctions and the number of roads in Nsk, as well as the indices of junctions where mayors home and work are located respectively. The i-th of the following m lines contains two integers ui and vi (1 ≤ ui, vi ≤ n, ui ≠ vi), meaning that this road connects junctions ui and vi directly. It is guaranteed that there is a path between any two junctions and no two roads connect the same pair of junctions.

Output

Print one integer — the number of pairs of junctions not connected by a direct road, such that building a road between these two junctions won't decrease the distance between junctions s and t.

Examples

Input

5 4 1 5
1 2
2 3
3 4
4 5


Output

0


Input

5 4 3 5
1 2
2 3
3 4
4 5


Output

5


Input

5 6 1 5
1 2
1 3
1 4
4 5
3 5
2 5


Output

3

## Categories

- dfs and similar
- graphs
- shortest paths

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5 4 3 5
1 2
2 3
3 4
4 5
```

**Output**:
```
5
```

### Example 2

**Input**:
```
5 6 1 5
1 2
1 3
1 4
4 5
3 5
2 5
```

**Output**:
```
3
```

### Example 3

**Input**:
```
5 4 1 5
1 2
2 3
3 4
4 5
```

**Output**:
```
0
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
