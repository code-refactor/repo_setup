# 1427_E. Xum

**ID:** 1427_e_xum_2840
**Difficulty:** 11

## Description

You have a blackboard and initially only an odd number x is written on it. Your goal is to write the number 1 on the blackboard.

You may write new numbers on the blackboard with the following two operations. 

  * You may take two numbers (not necessarily distinct) already on the blackboard and write their sum on the blackboard. The two numbers you have chosen remain on the blackboard. 
  * You may take two numbers (not necessarily distinct) already on the blackboard and write their [bitwise XOR](https://en.wikipedia.org/wiki/Bitwise_operation#XOR) on the blackboard. The two numbers you have chosen remain on the blackboard. 

Perform a sequence of operations such that at the end the number 1 is on the blackboard.

Input

The single line of the input contains the odd integer x (3 ≤ x ≤ 999,999).

Output

Print on the first line the number q of operations you perform. Then q lines should follow, each describing one operation. 

  * The "sum" operation is described by the line "a + b", where a, b must be integers already present on the blackboard. 
  * The "xor" operation is described by the line "a ^ b", where a, b must be integers already present on the blackboard. 

The operation symbol (+ or ^) must be separated from a, b by a whitespace.

You can perform at most 100,000 operations (that is, q≤ 100,000) and all numbers written on the blackboard must be in the range [0, 5⋅10^{18}]. It can be proven that under such restrictions the required sequence of operations exists. You can output any suitable sequence of operations.

Examples

Input


3


Output


5
3 + 3
3 ^ 6
3 + 5
3 + 6
8 ^ 9


Input


123


Output


10
123 + 123
123 ^ 246
141 + 123
246 + 123
264 ^ 369
121 + 246
367 ^ 369
30 + 30
60 + 60
120 ^ 121

## Categories

- bitmasks
- constructive algorithms
- math
- matrices
- number theory

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
```

**Output**:
```
5
3 + 3
3 ^ 6
3 + 5
3 + 6
8 ^ 9
```

### Example 2

**Input**:
```
123
```

**Output**:
```
10
123 + 123
123 ^ 246
141 + 123
246 + 123
264 ^ 369
121 + 246
367 ^ 369
30 + 30
60 + 60
120 ^ 121
```

### Example 3

**Input**:
```
804351
```

**Output**:
```
1146
804351 + 804351
804351 ^ 1608702
804351 ^ 1608702
1363457 + 1363457
2726914 ^ 1608702
804351 ^ 1608702
1363457 ^ 3217404
2480637 + 1608702
4089339 ^ 804351
3284996 ^ 3217404
804351 ^ 210936
1012231 + 3217404
4229635 ^ 804351
5033980 ^ 3217404
1608702 ^ 3217404
2726914 ^ 8247296
1608702 ^ 210936
1817606 ^ 8247296
5522434 + 6710278
12232712 ^ 210936
12165104 ^ 8247296
804351 ^ 3217404
4018691 ^ 210936
4089339 ^ 12863472
804351 ^ 3217404
4018691 ^ 210936
4089339 ^ 8247296
1639...
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
