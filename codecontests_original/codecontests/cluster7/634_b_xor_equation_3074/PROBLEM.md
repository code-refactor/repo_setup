# 634_B. XOR Equation

**ID:** 634_b_xor_equation_3074
**Difficulty:** 8

## Description

Two positive integers a and b have a sum of s and a bitwise XOR of x. How many possible values are there for the ordered pair (a, b)?

Input

The first line of the input contains two integers s and x (2 ≤ s ≤ 1012, 0 ≤ x ≤ 1012), the sum and bitwise xor of the pair of positive integers, respectively.

Output

Print a single integer, the number of solutions to the given conditions. If no solutions exist, print 0.

Examples

Input

9 5


Output

4


Input

3 3


Output

2


Input

5 2


Output

0

Note

In the first sample, we have the following solutions: (2, 7), (3, 6), (6, 3), (7, 2).

In the second sample, the only solutions are (1, 2) and (2, 1).

## Categories

- dp
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5 2
```

**Output**:
```
0
```

### Example 2

**Input**:
```
3 3
```

**Output**:
```
2
```

### Example 3

**Input**:
```
9 5
```

**Output**:
```
4
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
