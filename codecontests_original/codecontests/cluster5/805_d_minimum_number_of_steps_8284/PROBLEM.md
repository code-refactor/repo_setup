# 805_D. Minimum number of steps

**ID:** 805_d_minimum_number_of_steps_8284
**Difficulty:** 10

## Description

We have a string of letters 'a' and 'b'. We want to perform some operations on it. On each step we choose one of substrings "ab" in the string and replace it with the string "bba". If we have no "ab" as a substring, our job is done. Print the minimum number of steps we should perform to make our job done modulo 109 + 7.

The string "ab" appears as a substring if there is a letter 'b' right after the letter 'a' somewhere in the string.

Input

The first line contains the initial string consisting of letters 'a' and 'b' only with length from 1 to 106.

Output

Print the minimum number of steps modulo 109 + 7.

Examples

Input

ab


Output

1


Input

aab


Output

3

Note

The first example: "ab"  →  "bba".

The second example: "aab"  →  "abba"  →  "bbaba"  →  "bbbbaa".

## Categories

- combinatorics
- greedy
- implementation
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
aab
```

**Output**:
```
3
```

### Example 2

**Input**:
```
ab
```

**Output**:
```
1
```

### Example 3

**Input**:
```
aabbaababbabbbaabbaababaaaabbaaaabaaaaaababbaaaabaababbabbbb
```

**Output**:
```
436420225
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
