# 850_A. Five Dimensional Points

**ID:** 850_a_five_dimensional_points_3812
**Difficulty:** very hard

## Description

You are given set of n points in 5-dimensional space. The points are labeled from 1 to n. No two points coincide.

We will call point a bad if there are different points b and c, not equal to a, from the given set such that angle between vectors <image> and <image> is acute (i.e. strictly less than <image>). Otherwise, the point is called good.

The angle between vectors <image> and <image> in 5-dimensional space is defined as <image>, where <image> is the scalar product and <image> is length of <image>.

Given the list of points, print the indices of the good points in ascending order.

Input

The first line of input contains a single integer n (1 ≤ n ≤ 103) — the number of points.

The next n lines of input contain five integers ai, bi, ci, di, ei (|ai|, |bi|, |ci|, |di|, |ei| ≤ 103) — the coordinates of the i-th point. All points are distinct.

Output

First, print a single integer k — the number of good points.

Then, print k integers, each on their own line — the indices of the good points in ascending order.

Examples

Input

6
0 0 0 0 0
1 0 0 0 0
0 1 0 0 0
0 0 1 0 0
0 0 0 1 0
0 0 0 0 1


Output

1
1


Input

3
0 0 1 2 0
0 0 9 2 0
0 0 5 9 0


Output

0

Note

In the first sample, the first point forms exactly a <image> angle with all other pairs of points, so it is good.

In the second sample, along the cd plane, we can see the points look as follows:

<image>

We can see that all angles here are acute, so no points are good.

## Categories

- brute force
- geometry
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
0 0 1 2 0
0 0 9 2 0
0 0 5 9 0
```

**Output**:
```
0
```

### Example 2

**Input**:
```
6
0 0 0 0 0
1 0 0 0 0
0 1 0 0 0
0 0 1 0 0
0 0 0 1 0
0 0 0 0 1
```

**Output**:
```
1
1
```

### Example 3

**Input**:
```
10
0 -110 68 -51 -155
-85 -110 68 -51 -155
85 -70 51 68 -230
0 -40 51 68 75
0 5 -51 -68 -190
85 0 0 0 0
85 -115 -68 51 35
85 -75 -187 34 -40
-85 -110 -136 102 -155
85 -110 -17 119 -155
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
