# 1016_D. Vasya And The Matrix

**ID:** 1016_d_vasya_and_the_matrix_3445
**Difficulty:** 10

## Description

Now Vasya is taking an exam in mathematics. In order to get a good mark, Vasya needs to guess the matrix that the teacher has constructed!

Vasya knows that the matrix consists of n rows and m columns. For each row, he knows the xor (bitwise excluding or) of the elements in this row. The sequence a1, a2, ..., an denotes the xor of elements in rows with indices 1, 2, ..., n, respectively. Similarly, for each column, he knows the xor of the elements in this column. The sequence b1, b2, ..., bm denotes the xor of elements in columns with indices 1, 2, ..., m, respectively.

Help Vasya! Find a matrix satisfying the given constraints or tell him that there is no suitable matrix.

Input

The first line contains two numbers n and m (2 ≤ n, m ≤ 100) — the dimensions of the matrix.

The second line contains n numbers a1, a2, ..., an (0 ≤ ai ≤ 109), where ai is the xor of all elements in row i.

The third line contains m numbers b1, b2, ..., bm (0 ≤ bi ≤ 109), where bi is the xor of all elements in column i.

Output

If there is no matrix satisfying the given constraints in the first line, output "NO".

Otherwise, on the first line output "YES", and then n rows of m numbers in each ci1, ci2, ... , cim (0 ≤ cij ≤ 2·109) — the description of the matrix.

If there are several suitable matrices, it is allowed to print any of them.

Examples

Input

2 3
2 9
5 3 13


Output

YES
3 4 5
6 7 8


Input

3 3
1 7 6
2 15 12


Output

NO

## Categories

- constructive algorithms
- flows
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3 3
1 7 6
2 15 12
```

**Output**:
```
NO
```

### Example 2

**Input**:
```
2 3
2 9
5 3 13
```

**Output**:
```
YES
12 3 13
9 0 0
```

### Example 3

**Input**:
```
2 2
1 0
0 0
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
