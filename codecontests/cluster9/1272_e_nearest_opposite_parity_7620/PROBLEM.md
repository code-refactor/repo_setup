# 1272_E. Nearest Opposite Parity

**ID:** 1272_e_nearest_opposite_parity_7620
**Difficulty:** 11

## Description

You are given an array a consisting of n integers. In one move, you can jump from the position i to the position i - a_i (if 1 ≤ i - a_i) or to the position i + a_i (if i + a_i ≤ n).

For each position i from 1 to n you want to know the minimum the number of moves required to reach any position j such that a_j has the opposite parity from a_i (i.e. if a_i is odd then a_j has to be even and vice versa).

Input

The first line of the input contains one integer n (1 ≤ n ≤ 2 ⋅ 10^5) — the number of elements in a.

The second line of the input contains n integers a_1, a_2, ..., a_n (1 ≤ a_i ≤ n), where a_i is the i-th element of a.

Output

Print n integers d_1, d_2, ..., d_n, where d_i is the minimum the number of moves required to reach any position j such that a_j has the opposite parity from a_i (i.e. if a_i is odd then a_j has to be even and vice versa) or -1 if it is impossible to reach such a position.

Example

Input


10
4 5 7 6 7 5 4 4 6 4


Output


1 1 1 2 -1 1 1 3 1 1 

## Categories

- dfs and similar
- graphs
- shortest paths

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
10
4 5 7 6 7 5 4 4 6 4
```

**Output**:
```
1 1 1 2 -1 1 1 3 1 1
```

### Example 2

**Input**:
```
150
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2
```

**Output**:
```
149 148 147 146 145 144 143 142 141 140 139 138 137 136 135 134 133 132 131 130 129 128 127 126 125 124 123 122 121 120 119 118 117 116 115 114 113 112 111 110 109 108 107 106 105 104 103 102 101 100 99 98 97 96 95 94 93 92 91 90 89 88 87 86 85 84 83 82 81 80 79 78 77 76 75 74 73 72 71 70 69 68 67 66 65 64 63 62 61 60 59 58 57 56 55 54 53 52 51 50 49 48 47 46 45 44 43 42 41 40 39 38 37 36 35 34 33 32 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 1
```

### Example 3

**Input**:
```
100
7 9 5 3 5 3 3 7 4 3 5 7 9 7 3 9 5 3 7 5 5 9 3 3 3 9 5 7 3 5 7 3 5 3 9 7 7 7 5 7 7 7 7 9 9 7 3 3 3 3 9 5 7 9 9 3 3 9 9 9 9 5 5 7 9 5 9 5 3 3 7 7 5 5 9 9 5 3 3 5 9 7 9 5 4 9 7 9 7 7 7 9 5 3 3 3 3 3 9 3
```

**Output**:
```
14 3 14 13 12 1 12 13 1 11 2 11 10 11 12 11 10 11 10 11 10 9 10 11 10 9 10 9 10 9 8 9 8 9 8 9 8 7 8 9 8 9 8 7 6 7 8 7 8 7 6 7 6 5 8 7 6 3 6 5 4 3 4 7 4 5 2 5 4 3 6 3 6 3 4 1 4 5 2 1 4 5 4 3 1 5 2 3 6 5 4 5 4 5 6 5 6 7 6 7
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
