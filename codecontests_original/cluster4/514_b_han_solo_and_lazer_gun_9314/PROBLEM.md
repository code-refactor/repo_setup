# 514_B. Han Solo and Lazer Gun

**ID:** 514_b_han_solo_and_lazer_gun_9314
**Difficulty:** 8

## Description

There are n Imperial stormtroopers on the field. The battle field is a plane with Cartesian coordinate system. Each stormtrooper is associated with his coordinates (x, y) on this plane. 

Han Solo has the newest duplex lazer gun to fight these stormtroopers. It is situated at the point (x0, y0). In one shot it can can destroy all the stormtroopers, situated on some line that crosses point (x0, y0).

Your task is to determine what minimum number of shots Han Solo needs to defeat all the stormtroopers.

The gun is the newest invention, it shoots very quickly and even after a very large number of shots the stormtroopers don't have enough time to realize what's happening and change their location. 

Input

The first line contains three integers n, x0 и y0 (1 ≤ n ≤ 1000,  - 104 ≤ x0, y0 ≤ 104) — the number of stormtroopers on the battle field and the coordinates of your gun.

Next n lines contain two integers each xi, yi ( - 104 ≤ xi, yi ≤ 104) — the coordinates of the stormtroopers on the battlefield. It is guaranteed that no stormtrooper stands at the same point with the gun. Multiple stormtroopers can stand at the same point.

Output

Print a single integer — the minimum number of shots Han Solo needs to destroy all the stormtroopers. 

Examples

Input

4 0 0
1 1
2 2
2 0
-1 -1


Output

2


Input

2 1 2
1 1
1 0


Output

1

Note

Explanation to the first and second samples from the statement, respectively: 

<image>

## Categories

- brute force
- data structures
- geometry
- implementation
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2 1 2
1 1
1 0
```

**Output**:
```
1
```

### Example 2

**Input**:
```
4 0 0
1 1
2 2
2 0
-1 -1
```

**Output**:
```
2
```

### Example 3

**Input**:
```
2 -10000 -10000
9998 9999
9999 10000
```

**Output**:
```
2
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
