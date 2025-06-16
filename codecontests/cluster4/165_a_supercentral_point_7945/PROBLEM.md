# 165_A. Supercentral Point

**ID:** 165_a_supercentral_point_7945
**Difficulty:** very hard

## Description

One day Vasya painted a Cartesian coordinate system on a piece of paper and marked some set of points (x1, y1), (x2, y2), ..., (xn, yn). Let's define neighbors for some fixed point from the given set (x, y): 

  * point (x', y') is (x, y)'s right neighbor, if x' > x and y' = y
  * point (x', y') is (x, y)'s left neighbor, if x' < x and y' = y
  * point (x', y') is (x, y)'s lower neighbor, if x' = x and y' < y
  * point (x', y') is (x, y)'s upper neighbor, if x' = x and y' > y



We'll consider point (x, y) from the given set supercentral, if it has at least one upper, at least one lower, at least one left and at least one right neighbor among this set's points.

Vasya marked quite many points on the paper. Analyzing the picture manually is rather a challenge, so Vasya asked you to help him. Your task is to find the number of supercentral points in the given set.

Input

The first input line contains the only integer n (1 ≤ n ≤ 200) — the number of points in the given set. Next n lines contain the coordinates of the points written as "x y" (without the quotes) (|x|, |y| ≤ 1000), all coordinates are integers. The numbers in the line are separated by exactly one space. It is guaranteed that all points are different.

Output

Print the only number — the number of supercentral points of the given set.

Examples

Input

8
1 1
4 2
3 1
1 2
0 2
0 1
1 0
1 3


Output

2


Input

5
0 0
0 1
1 0
0 -1
-1 0


Output

1

Note

In the first sample the supercentral points are only points (1, 1) and (1, 2).

In the second sample there is one supercental point — point (0, 0).

## Categories

- implementation

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
8
1 1
4 2
3 1
1 2
0 2
0 1
1 0
1 3
```

**Output**:
```
2
```

### Example 2

**Input**:
```
5
0 0
0 1
1 0
0 -1
-1 0
```

**Output**:
```
1
```

### Example 3

**Input**:
```
1
487 550
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
