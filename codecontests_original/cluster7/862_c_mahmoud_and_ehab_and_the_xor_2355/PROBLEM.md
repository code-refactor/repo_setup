# 862_C. Mahmoud and Ehab and the xor

**ID:** 862_c_mahmoud_and_ehab_and_the_xor_2355
**Difficulty:** 9

## Description

Mahmoud and Ehab are on the third stage of their adventures now. As you know, Dr. Evil likes sets. This time he won't show them any set from his large collection, but will ask them to create a new set to replenish his beautiful collection of sets.

Dr. Evil has his favorite evil integer x. He asks Mahmoud and Ehab to find a set of n distinct non-negative integers such the bitwise-xor sum of the integers in it is exactly x. Dr. Evil doesn't like big numbers, so any number in the set shouldn't be greater than 106.

Input

The only line contains two integers n and x (1 ≤ n ≤ 105, 0 ≤ x ≤ 105) — the number of elements in the set and the desired bitwise-xor, respectively.

Output

If there is no such set, print "NO" (without quotes).

Otherwise, on the first line print "YES" (without quotes) and on the second line print n distinct integers, denoting the elements in the set is any order. If there are multiple solutions you can print any of them.

Examples

Input

5 5


Output

YES
1 2 4 5 7

Input

3 6


Output

YES
1 2 5

Note

You can read more about the bitwise-xor operation here: <https://en.wikipedia.org/wiki/Bitwise_operation#XOR>

For the first sample <image>.

For the second sample <image>.

## Categories

- constructive algorithms

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3 6
```

**Output**:
```
YES
0 131072 131078
```

### Example 2

**Input**:
```
5 5
```

**Output**:
```
YES
1 2 0 131072 131078
```

### Example 3

**Input**:
```
3 3
```

**Output**:
```
YES
0 131072 131075
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
