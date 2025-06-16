# 1228_E. Another Filling the Grid

**ID:** 1228_e_another_filling_the_grid_12616
**Difficulty:** 11

## Description

You have n × n square grid and an integer k. Put an integer in each cell while satisfying the conditions below.

  * All numbers in the grid should be between 1 and k inclusive. 
  * Minimum number of the i-th row is 1 (1 ≤ i ≤ n). 
  * Minimum number of the j-th column is 1 (1 ≤ j ≤ n). 



Find the number of ways to put integers in the grid. Since the answer can be very large, find the answer modulo (10^{9} + 7).

<image> These are the examples of valid and invalid grid when n=k=2. 

Input

The only line contains two integers n and k (1 ≤ n ≤ 250, 1 ≤ k ≤ 10^{9}).

Output

Print the answer modulo (10^{9} + 7).

Examples

Input


2 2


Output


7


Input


123 456789


Output


689974806

Note

In the first example, following 7 cases are possible.

<image>

In the second example, make sure you print the answer modulo (10^{9} + 7).

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
123 456789
```

**Output**:
```
689974806
```

### Example 2

**Input**:
```
2 2
```

**Output**:
```
7
```

### Example 3

**Input**:
```
220 51931060
```

**Output**:
```
944377763
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
