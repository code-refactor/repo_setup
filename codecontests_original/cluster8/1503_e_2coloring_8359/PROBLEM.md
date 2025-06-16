# 1503_E. 2-Coloring

**ID:** 1503_e_2coloring_8359
**Difficulty:** 11

## Description

There is a grid with n rows and m columns. Every cell of the grid should be colored either blue or yellow.

A coloring of the grid is called stupid if every row has exactly one segment of blue cells and every column has exactly one segment of yellow cells.

In other words, every row must have at least one blue cell, and all blue cells in a row must be consecutive. Similarly, every column must have at least one yellow cell, and all yellow cells in a column must be consecutive.

<image> An example of a stupid coloring.  <image> Examples of clever colorings. The first coloring is missing a blue cell in the second row, and the second coloring has two yellow segments in the second column. 

How many stupid colorings of the grid are there? Two colorings are considered different if there is some cell that is colored differently.

Input

The only line contains two integers n, m (1≤ n, m≤ 2021).

Output

Output a single integer — the number of stupid colorings modulo 998244353.

Examples

Input


2 2


Output


2


Input


4 3


Output


294


Input


2020 2021


Output


50657649

Note

In the first test case, these are the only two stupid 2× 2 colorings.

<image>

## Categories

- combinatorics
- dp
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2 2
```

**Output**:
```
2
```

### Example 2

**Input**:
```
4 3
```

**Output**:
```
294
```

### Example 3

**Input**:
```
2020 2021
```

**Output**:
```
50657649
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
