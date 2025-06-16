# 938_E. Max History

**ID:** 938_e_max_history_10478
**Difficulty:** 11

## Description

You are given an array a of length n. We define fa the following way:

  * Initially fa = 0, M = 1; 
  * for every 2 ≤ i ≤ n if aM < ai then we set fa = fa + aM and then set M = i. 



Calculate the sum of fa over all n! permutations of the array a modulo 109 + 7.

Note: two elements are considered different if their indices differ, so for every array a there are exactly n! permutations.

Input

The first line contains integer n (1 ≤ n ≤ 1 000 000) — the size of array a.

Second line contains n integers a1, a2, ..., an (1 ≤ ai ≤ 109).

Output

Print the only integer, the sum of fa over all n! permutations of the array a modulo 109 + 7.

Examples

Input

2
1 3


Output

1

Input

3
1 1 2


Output

4

Note

For the second example all the permutations are:

  * p = [1, 2, 3] : fa is equal to 1; 
  * p = [1, 3, 2] : fa is equal to 1; 
  * p = [2, 1, 3] : fa is equal to 1; 
  * p = [2, 3, 1] : fa is equal to 1; 
  * p = [3, 1, 2] : fa is equal to 0; 
  * p = [3, 2, 1] : fa is equal to 0. 



Where p is the array of the indices of initial array a. The sum of fa is equal to 4.

## Categories

- combinatorics
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2
1 3
```

**Output**:
```
1
```

### Example 2

**Input**:
```
3
1 1 2
```

**Output**:
```
4
```

### Example 3

**Input**:
```
7
177679021 237356752 791250000 455912656 693129227 678510224 60382864
```

**Output**:
```
14393405
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
