# 289_E. Polo the Penguin and XOR operation

**ID:** 289_e_polo_the_penguin_and_xor_operation_6598
**Difficulty:** 11

## Description

Little penguin Polo likes permutations. But most of all he likes permutations of integers from 0 to n, inclusive.

For permutation p = p0, p1, ..., pn, Polo has defined its beauty — number <image>.

Expression <image> means applying the operation of bitwise excluding "OR" to numbers x and y. This operation exists in all modern programming languages, for example, in language C++ and Java it is represented as "^" and in Pascal — as "xor".

Help him find among all permutations of integers from 0 to n the permutation with the maximum beauty.

Input

The single line contains a positive integer n (1 ≤ n ≤ 106).

Output

In the first line print integer m the maximum possible beauty. In the second line print any permutation of integers from 0 to n with the beauty equal to m.

If there are several suitable permutations, you are allowed to print any of them.

Examples

Input

4


Output

20
0 2 1 4 3

## Categories

- implementation
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4
```

**Output**:
```
20
0 2 1 4 3
```

### Example 2

**Input**:
```
13
```

**Output**:
```
182
1 0 13 12 11 10 9 8 7 6 5 4 3 2
```

### Example 3

**Input**:
```
128
```

**Output**:
```
16512
0 126 125 124 123 122 121 120 119 118 117 116 115 114 113 112 111 110 109 108 107 106 105 104 103 102 101 100 99 98 97 96 95 94 93 92 91 90 89 88 87 86 85 84 83 82 81 80 79 78 77 76 75 74 73 72 71 70 69 68 67 66 65 64 63 62 61 60 59 58 57 56 55 54 53 52 51 50 49 48 47 46 45 44 43 42 41 40 39 38 37 36 35 34 33 32 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 128 127
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
