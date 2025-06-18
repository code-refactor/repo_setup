# 1516_B. AGAGA XOOORRR

**ID:** 1516_b_agaga_xooorrr_3468
**Difficulty:** 8

## Description

Baby Ehab is known for his love for a certain operation. He has an array a of length n, and he decided to keep doing the following operation on it: 

  * he picks 2 adjacent elements; he then removes them and places a single integer in their place: their [bitwise XOR](https://en.wikipedia.org/wiki/Bitwise_operation#XOR). Note that the length of the array decreases by one. 



Now he asks you if he can make all elements of the array equal. Since babies like to make your life harder, he requires that you leave at least 2 elements remaining.

Input

The first line contains an integer t (1 ≤ t ≤ 15) — the number of test cases you need to solve.

The first line of each test case contains an integers n (2 ≤ n ≤ 2000) — the number of elements in the array a.

The second line contains n space-separated integers a_1, a_2, …, a_{n} (0 ≤ a_i < 2^{30}) — the elements of the array a.

Output

If Baby Ehab can make all elements equal while leaving at least 2 elements standing, print "YES". Otherwise, print "NO".

Example

Input


2
3
0 2 2
4
2 3 1 10


Output


YES
NO

Note

In the first sample, he can remove the first 2 elements, 0 and 2, and replace them by 0 ⊕ 2=2. The array will be [2,2], so all the elements are equal.

In the second sample, there's no way to make all the elements equal.

## Categories

- bitmasks
- brute force
- dp
- greedy

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2
3
0 2 2
4
2 3 1 10
```

**Output**:
```
YES
NO
```

### Example 2

**Input**:
```
1
5
3 3 3 2 2
```

**Output**:
```
YES
```

### Example 3

**Input**:
```
1
4
3 3 3 0
```

**Output**:
```
YES
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
