# 1342_E. Placing Rooks

**ID:** 1342_e_placing_rooks_855
**Difficulty:** 11

## Description

Calculate the number of ways to place n rooks on n × n chessboard so that both following conditions are met:

  * each empty cell is under attack; 
  * exactly k pairs of rooks attack each other. 



An empty cell is under attack if there is at least one rook in the same row or at least one rook in the same column. Two rooks attack each other if they share the same row or column, and there are no other rooks between them. For example, there are only two pairs of rooks that attack each other in the following picture:

<image> One of the ways to place the rooks for n = 3 and k = 2

Two ways to place the rooks are considered different if there exists at least one cell which is empty in one of the ways but contains a rook in another way.

The answer might be large, so print it modulo 998244353.

Input

The only line of the input contains two integers n and k (1 ≤ n ≤ 200000; 0 ≤ k ≤ (n(n - 1))/(2)).

Output

Print one integer — the number of ways to place the rooks, taken modulo 998244353.

Examples

Input


3 2


Output


6


Input


3 3


Output


0


Input


4 0


Output


24


Input


1337 42


Output


807905441

## Categories

- combinatorics
- fft
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4 0
```

**Output**:
```
24
```

### Example 2

**Input**:
```
3 2
```

**Output**:
```
6
```

### Example 3

**Input**:
```
1337 42
```

**Output**:
```
807905441
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
