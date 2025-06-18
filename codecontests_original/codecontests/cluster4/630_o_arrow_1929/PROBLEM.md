# 630_O. Arrow

**ID:** 630_o_arrow_1929
**Difficulty:** 22

## Description

Petya has recently started working as a programmer in the IT city company that develops computer games.

Besides game mechanics implementation to create a game it is necessary to create tool programs that can be used by game designers to create game levels. Petya's first assignment is to create a tool that allows to paint different arrows on the screen.

A user of this tool will choose a point on the screen, specify a vector (the arrow direction) and vary several parameters to get the required graphical effect. In the first version of the program Petya decided to limit parameters of the arrow by the following: a point with coordinates (px, py), a nonzero vector with coordinates (vx, vy), positive scalars a, b, c, d, a > c.

The produced arrow should have the following properties. The arrow consists of a triangle and a rectangle. The triangle is isosceles with base of length a and altitude of length b perpendicular to the base. The rectangle sides lengths are c and d. Point (px, py) is situated in the middle of the triangle base and in the middle of side of rectangle that has length c. Area of intersection of the triangle and the rectangle is zero. The direction from (px, py) point to the triangle vertex opposite to base containing the point coincides with direction of (vx, vy) vector.

Enumerate the arrow points coordinates in counter-clockwise order starting from the tip.

<image>

Input

The only line of the input contains eight integers px, py, vx, vy ( - 1000 ≤ px, py, vx, vy ≤ 1000, vx2 + vy2 > 0), a, b, c, d (1 ≤ a, b, c, d ≤ 1000, a > c).

Output

Output coordinates of the arrow points in counter-clockwise order. Each line should contain two coordinates, first x, then y. Relative or absolute error should not be greater than 10 - 9.

Examples

Input

8 8 0 2 8 3 4 5


Output

8.000000000000 11.000000000000
4.000000000000 8.000000000000
6.000000000000 8.000000000000
6.000000000000 3.000000000000
10.000000000000 3.000000000000
10.000000000000 8.000000000000
12.000000000000 8.000000000000

## Categories

- geometry

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
8 8 0 2 8 3 4 5
```

**Output**:
```
8.0000000000000000000000000 11.0000000000000000000000000
4.0000000000000000000000000 8.0000000000000000000000000
6.0000000000000000000000000 8.0000000000000000000000000
6.0000000000000000000000000 3.0000000000000000000000000
10.0000000000000000000000000 3.0000000000000000000000000
10.0000000000000000000000000 8.0000000000000000000000000
12.0000000000000000000000000 8.0000000000000000000000000
```

### Example 2

**Input**:
```
10 10 -7 0 5 8 2 11
```

**Output**:
```
2.0000000000000000000000000 10.0000000000000000000000000
10.0000000000000000000000000 7.5000000000000000000000000
10.0000000000000000000000000 9.0000000000000000000000000
21.0000000000000000000000000 9.0000000000000000000000000
21.0000000000000000000000000 11.0000000000000000000000000
10.0000000000000000000000000 11.0000000000000000000000000
10.0000000000000000000000000 12.5000000000000000000000000
```

### Example 3

**Input**:
```
870 396 187 223 444 202 222 732
```

**Output**:
```
999.7945324433952405951409048 550.7817151597707949206572664
699.8933625471825917263579697 538.6454762496719970710223890
784.9466812735912958354234092 467.3227381248359985355111945
314.6021379638620081853339627 -93.5694178006700504057757684
484.7087754166794164589759930 -236.2148940503420475045537330
955.0533187264087041645765908 324.6772618751640014644888055
1040.1066374528174083291531815 253.3545237503280029150998232
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
