# 1438_D. Powerful Ksenia

**ID:** 1438_d_powerful_ksenia_5652
**Difficulty:** 10

## Description

Ksenia has an array a consisting of n positive integers a_1, a_2, …, a_n. 

In one operation she can do the following: 

  * choose three distinct indices i, j, k, and then 
  * change all of a_i, a_j, a_k to a_i ⊕ a_j ⊕ a_k simultaneously, where ⊕ denotes the [bitwise XOR operation](https://en.wikipedia.org/wiki/Bitwise_operation#XOR). 



She wants to make all a_i equal in at most n operations, or to determine that it is impossible to do so. She wouldn't ask for your help, but please, help her!

Input

The first line contains one integer n (3 ≤ n ≤ 10^5) — the length of a.

The second line contains n integers, a_1, a_2, …, a_n (1 ≤ a_i ≤ 10^9) — elements of a.

Output

Print YES or NO in the first line depending on whether it is possible to make all elements equal in at most n operations.

If it is possible, print an integer m (0 ≤ m ≤ n), which denotes the number of operations you do.

In each of the next m lines, print three distinct integers i, j, k, representing one operation. 

If there are many such operation sequences possible, print any. Note that you do not have to minimize the number of operations.

Examples

Input


5
4 2 1 7 2


Output


YES
1
1 3 4

Input


4
10 4 49 22


Output


NO

Note

In the first example, the array becomes [4 ⊕ 1 ⊕ 7, 2, 4 ⊕ 1 ⊕ 7, 4 ⊕ 1 ⊕ 7, 2] = [2, 2, 2, 2, 2].

## Categories

- bitmasks
- constructive algorithms
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
5
4 2 1 7 2
```

**Output**:
```
YES
4
1 2 3
3 4 5
1 2 5
3 4 5
```

### Example 2

**Input**:
```
4
10 4 49 22
```

**Output**:
```
NO
```

### Example 3

**Input**:
```
4
1 1 1 1
```

**Output**:
```
YES
1
1 2 3
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
