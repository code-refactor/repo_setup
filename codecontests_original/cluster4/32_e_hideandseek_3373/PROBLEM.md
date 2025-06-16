# 32_E. Hide-and-Seek

**ID:** 32_e_hideandseek_3373
**Difficulty:** 11

## Description

Victor and Peter are playing hide-and-seek. Peter has hidden, and Victor is to find him. In the room where they are playing, there is only one non-transparent wall and one double-sided mirror. Victor and Peter are points with coordinates (xv, yv) and (xp, yp) respectively. The wall is a segment joining points with coordinates (xw, 1, yw, 1) and (xw, 2, yw, 2), the mirror — a segment joining points (xm, 1, ym, 1) and (xm, 2, ym, 2).

If an obstacle has a common point with a line of vision, it's considered, that the boys can't see each other with this line of vision. If the mirror has a common point with the line of vision, it's considered, that the boys can see each other in the mirror, i.e. reflection takes place. The reflection process is governed by laws of physics — the angle of incidence is equal to the angle of reflection. The incident ray is in the same half-plane as the reflected ray, relative to the mirror. I.e. to see each other Victor and Peter should be to the same side of the line, containing the mirror (see example 1). If the line of vision is parallel to the mirror, reflection doesn't take place, and the mirror isn't regarded as an obstacle (see example 4).

Victor got interested if he can see Peter, while standing at the same spot. Help him solve this problem.

Input

The first line contains two numbers xv and yv — coordinates of Victor.

The second line contains two numbers xp and yp — coordinates of Peter.

The third line contains 4 numbers xw, 1, yw, 1, xw, 2, yw, 2 — coordinates of the wall.

The forth line contains 4 numbers xm, 1, ym, 1, xm, 2, ym, 2 — coordinates of the mirror.

All the coordinates are integer numbers, and don't exceed 104 in absolute value. It's guaranteed, that the segments don't have common points, Victor and Peter are not on any of the segments, coordinates of Victor and Peter aren't the same, the segments don't degenerate into points.

Output

Output YES, if Victor can see Peter without leaving the initial spot. Otherwise output NO.

Examples

Input

-1 3
1 3
0 2 0 4
0 0 0 1


Output

NO


Input

0 0
1 1
0 1 1 0
-100 -100 -101 -101


Output

NO


Input

0 0
1 1
0 1 1 0
-1 1 1 3


Output

YES


Input

0 0
10 0
100 100 101 101
1 0 3 0


Output

YES

## Categories

- geometry
- implementation

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
0 0
10 0
100 100 101 101
1 0 3 0
```

**Output**:
```
YES
```

### Example 2

**Input**:
```
-1 3
1 3
0 2 0 4
0 0 0 1
```

**Output**:
```
NO
```

### Example 3

**Input**:
```
0 0
1 1
0 1 1 0
-100 -100 -101 -101
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
