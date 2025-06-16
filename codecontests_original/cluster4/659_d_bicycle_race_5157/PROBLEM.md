# 659_D. Bicycle Race

**ID:** 659_d_bicycle_race_5157
**Difficulty:** 10

## Description

Maria participates in a bicycle race.

The speedway takes place on the shores of Lake Lucerne, just repeating its contour. As you know, the lake shore consists only of straight sections, directed to the north, south, east or west.

Let's introduce a system of coordinates, directing the Ox axis from west to east, and the Oy axis from south to north. As a starting position of the race the southernmost point of the track is selected (and if there are several such points, the most western among them). The participants start the race, moving to the north. At all straight sections of the track, the participants travel in one of the four directions (north, south, east or west) and change the direction of movement only in bends between the straight sections. The participants, of course, never turn back, that is, they do not change the direction of movement from north to south or from east to west (or vice versa).

Maria is still young, so she does not feel confident at some turns. Namely, Maria feels insecure if at a failed or untimely turn, she gets into the water. In other words, Maria considers the turn dangerous if she immediately gets into the water if it is ignored.

Help Maria get ready for the competition — determine the number of dangerous turns on the track.

Input

The first line of the input contains an integer n (4 ≤ n ≤ 1000) — the number of straight sections of the track.

The following (n + 1)-th line contains pairs of integers (xi, yi) ( - 10 000 ≤ xi, yi ≤ 10 000). The first of these points is the starting position. The i-th straight section of the track begins at the point (xi, yi) and ends at the point (xi + 1, yi + 1).

It is guaranteed that:

  * the first straight section is directed to the north; 
  * the southernmost (and if there are several, then the most western of among them) point of the track is the first point; 
  * the last point coincides with the first one (i.e., the start position); 
  * any pair of straight sections of the track has no shared points (except for the neighboring ones, they share exactly one point); 
  * no pair of points (except for the first and last one) is the same; 
  * no two adjacent straight sections are directed in the same direction or in opposite directions. 

Output

Print a single integer — the number of dangerous turns on the track.

Examples

Input

6
0 0
0 1
1 1
1 2
2 2
2 0
0 0


Output

1


Input

16
1 1
1 5
3 5
3 7
2 7
2 9
6 9
6 7
5 7
5 3
4 3
4 4
3 4
3 2
5 2
5 1
1 1


Output

6

Note

The first sample corresponds to the picture:

<image>

The picture shows that you can get in the water under unfortunate circumstances only at turn at the point (1, 1). Thus, the answer is 1.

## Categories

- geometry
- implementation
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
16
1 1
1 5
3 5
3 7
2 7
2 9
6 9
6 7
5 7
5 3
4 3
4 4
3 4
3 2
5 2
5 1
1 1
```

**Output**:
```
6
```

### Example 2

**Input**:
```
6
0 0
0 1
1 1
1 2
2 2
2 0
0 0
```

**Output**:
```
1
```

### Example 3

**Input**:
```
24
-10000 -10000
-10000 9998
9998 9998
9998 -10000
-6364 -10000
-6364 6362
6362 6362
6362 -6364
-2728 -6364
-2728 2726
2726 2726
2726 -910
908 -910
908 908
-910 908
-910 -4546
4544 -4546
4544 4544
-4546 4544
-4546 -8182
8180 -8182
8180 8180
-8182 8180
-8182 -10000
-10000 -10000
```

**Output**:
```
10
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
