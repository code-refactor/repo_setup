# 1312_D. Count the Arrays

**ID:** 1312_d_count_the_arrays_4501
**Difficulty:** 10

## Description

Your task is to calculate the number of arrays such that:

  * each array contains n elements; 
  * each element is an integer from 1 to m; 
  * for each array, there is exactly one pair of equal elements; 
  * for each array a, there exists an index i such that the array is strictly ascending before the i-th element and strictly descending after it (formally, it means that a_j < a_{j + 1}, if j < i, and a_j > a_{j + 1}, if j ≥ i). 

Input

The first line contains two integers n and m (2 ≤ n ≤ m ≤ 2 ⋅ 10^5).

Output

Print one integer — the number of arrays that meet all of the aforementioned conditions, taken modulo 998244353.

Examples

Input


3 4


Output


6


Input


3 5


Output


10


Input


42 1337


Output


806066790


Input


100000 200000


Output


707899035

Note

The arrays in the first example are:

  * [1, 2, 1]; 
  * [1, 3, 1]; 
  * [1, 4, 1]; 
  * [2, 3, 2]; 
  * [2, 4, 2]; 
  * [3, 4, 3]. 

## Categories

- combinatorics
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
100000 200000
```

**Output**:
```
707899035
```

### Example 2

**Input**:
```
3 4
```

**Output**:
```
6
```

### Example 3

**Input**:
```
3 5
```

**Output**:
```
10
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
