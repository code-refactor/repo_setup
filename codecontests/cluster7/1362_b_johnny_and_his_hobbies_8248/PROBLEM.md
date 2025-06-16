# 1362_B. Johnny and His Hobbies

**ID:** 1362_b_johnny_and_his_hobbies_8248
**Difficulty:** 8

## Description

Among Johnny's numerous hobbies, there are two seemingly harmless ones: applying bitwise operations and sneaking into his dad's office. As it is usually the case with small children, Johnny is unaware that combining these two activities can get him in a lot of trouble.

There is a set S containing very important numbers on his dad's desk. The minute Johnny heard about it, he decided that it's a good idea to choose a positive integer k and replace each element s of the set S with s ⊕ k (⊕ denotes the [exclusive or](https://en.wikipedia.org/wiki/Exclusive_or#Computer_science) operation). 

Help him choose such k that Johnny's dad will not see any difference after his son is done playing (i.e. Johnny will get the same set as before playing). It is possible that no such number exists. It is also possible that there are many of them. In such a case, output the smallest one. Note that the order of elements in a set doesn't matter, i.e. set \{1, 2, 3\} equals to set \{2, 1, 3\}.

Formally, find the smallest positive integer k such that \\{s ⊕ k | s ∈ S\} = S or report that there is no such number.

For example, if S = \{1, 3, 4\} and k = 2, new set will be equal to \{3, 1, 6\}. If S = \{0, 1, 2, 3\} and k = 1, after playing set will stay the same.

Input

In the first line of input, there is a single integer t (1 ≤ t ≤ 1024), the number of test cases. In the next lines, t test cases follow. Each of them consists of two lines. 

In the first line there is a single integer n (1 ≤ n ≤ 1024) denoting the number of elements in set S. Second line consists of n distinct integers s_i (0 ≤ s_i < 1024), elements of S.

It is guaranteed that the sum of n over all test cases will not exceed 1024.

Output

Print t lines; i-th line should contain the answer to the i-th test case, the minimal positive integer k satisfying the conditions or -1 if no such k exists.

Example

Input


6
4
1 0 2 3
6
10 7 14 8 3 12
2
0 2
3
1 2 3
6
1 4 6 10 11 12
2
0 1023


Output


1
4
2
-1
-1
1023

Note

In the first test case, the answer is 1 because it is a minimum positive integer and it satisfies all the conditions.

## Categories

- bitmasks
- brute force

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
6
4
1 0 2 3
6
10 7 14 8 3 12
2
0 2
3
1 2 3
6
1 4 6 10 11 12
2
0 1023
```

**Output**:
```
1
4
2
-1
-1
1023
```

### Example 2

**Input**:
```
6
4
1 0 2 3
6
10 7 14 8 0 12
2
0 2
3
1 2 3
6
1 4 6 10 11 12
2
0 1023
```

**Output**:
```
1
-1
2
-1
-1
1023
```

### Example 3

**Input**:
```
6
4
1 0 2 5
6
10 7 14 8 0 12
2
0 2
3
1 2 3
6
1 4 6 10 11 12
2
0 1023
```

**Output**:
```
-1
-1
2
-1
-1
1023
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
