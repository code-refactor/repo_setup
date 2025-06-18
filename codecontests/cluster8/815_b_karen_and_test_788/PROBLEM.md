# 815_B. Karen and Test

**ID:** 815_b_karen_and_test_788
**Difficulty:** 8

## Description

Karen has just arrived at school, and she has a math test today!

<image>

The test is about basic addition and subtraction. Unfortunately, the teachers were too busy writing tasks for Codeforces rounds, and had no time to make an actual test. So, they just put one question in the test that is worth all the points.

There are n integers written on a row. Karen must alternately add and subtract each pair of adjacent integers, and write down the sums or differences on the next row. She must repeat this process on the values on the next row, and so on, until only one integer remains. The first operation should be addition.

Note that, if she ended the previous row by adding the integers, she should start the next row by subtracting, and vice versa.

The teachers will simply look at the last integer, and then if it is correct, Karen gets a perfect score, otherwise, she gets a zero for the test.

Karen has studied well for this test, but she is scared that she might make a mistake somewhere and it will cause her final answer to be wrong. If the process is followed, what number can she expect to be written on the last row?

Since this number can be quite large, output only the non-negative remainder after dividing it by 109 + 7.

Input

The first line of input contains a single integer n (1 ≤ n ≤ 200000), the number of numbers written on the first row.

The next line contains n integers. Specifically, the i-th one among these is ai (1 ≤ ai ≤ 109), the i-th number on the first row.

Output

Output a single integer on a line by itself, the number on the final row after performing the process above.

Since this number can be quite large, print only the non-negative remainder after dividing it by 109 + 7.

Examples

Input

5
3 6 9 12 15


Output

36


Input

4
3 7 5 2


Output

1000000006

Note

In the first test case, the numbers written on the first row are 3, 6, 9, 12 and 15.

Karen performs the operations as follows:

<image>

The non-negative remainder after dividing the final number by 109 + 7 is still 36, so this is the correct output.

In the second test case, the numbers written on the first row are 3, 7, 5 and 2.

Karen performs the operations as follows:

<image>

The non-negative remainder after dividing the final number by 109 + 7 is 109 + 6, so this is the correct output.

## Categories

- brute force
- combinatorics
- constructive algorithms
- math

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4
3 7 5 2
```

**Output**:
```
1000000006
```

### Example 2

**Input**:
```
5
3 6 9 12 15
```

**Output**:
```
36
```

### Example 3

**Input**:
```
6
58376259 643910770 5887448 757703054 544067926 902981667
```

**Output**:
```
676517605
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
