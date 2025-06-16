# 1294_C. Product of Three Numbers

**ID:** 1294_c_product_of_three_numbers_4292
**Difficulty:** 9

## Description

You are given one integer number n. Find three distinct integers a, b, c such that 2 ≤ a, b, c and a ⋅ b ⋅ c = n or say that it is impossible to do it.

If there are several answers, you can print any.

You have to answer t independent test cases.

Input

The first line of the input contains one integer t (1 ≤ t ≤ 100) — the number of test cases.

The next n lines describe test cases. The i-th test case is given on a new line as one integer n (2 ≤ n ≤ 10^9).

Output

For each test case, print the answer on it. Print "NO" if it is impossible to represent n as a ⋅ b ⋅ c for some distinct integers a, b, c such that 2 ≤ a, b, c.

Otherwise, print "YES" and any possible such representation.

Example

Input


5
64
32
97
2
12345


Output


YES
2 4 8 
NO
NO
NO
YES
3 5 823 

## Categories

- greedy
- math
- number theory

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5
64
32
97
2
12345
```

**Output**:
```
YES
2 4 8
NO
NO
NO
YES
3 5 823
```

### Example 2

**Input**:
```
6
10
10
10
10
10
10
```

**Output**:
```
NO
NO
NO
NO
NO
NO
```

### Example 3

**Input**:
```
1
1112
```

**Output**:
```
YES
2 4 139
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
