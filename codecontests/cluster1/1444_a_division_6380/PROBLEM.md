# 1444_A. Division

**ID:** 1444_a_division_6380
**Difficulty:** very hard

## Description

Oleg's favorite subjects are History and Math, and his favorite branch of mathematics is division.

To improve his division skills, Oleg came up with t pairs of integers p_i and q_i and for each pair decided to find the greatest integer x_i, such that: 

  * p_i is divisible by x_i; 
  * x_i is not divisible by q_i. 

Oleg is really good at division and managed to find all the answers quickly, how about you?

Input

The first line contains an integer t (1 ≤ t ≤ 50) — the number of pairs.

Each of the following t lines contains two integers p_i and q_i (1 ≤ p_i ≤ 10^{18}; 2 ≤ q_i ≤ 10^{9}) — the i-th pair of integers.

Output

Print t integers: the i-th integer is the largest x_i such that p_i is divisible by x_i, but x_i is not divisible by q_i.

One can show that there is always at least one value of x_i satisfying the divisibility conditions for the given constraints.

Example

Input


3
10 4
12 6
179 822


Output


10
4
179

Note

For the first pair, where p_1 = 10 and q_1 = 4, the answer is x_1 = 10, since it is the greatest divisor of 10 and 10 is not divisible by 4.

For the second pair, where p_2 = 12 and q_2 = 6, note that 

  * 12 is not a valid x_2, since 12 is divisible by q_2 = 6; 
  * 6 is not valid x_2 as well: 6 is also divisible by q_2 = 6. 

The next available divisor of p_2 = 12 is 4, which is the answer, since 4 is not divisible by 6.

## Categories

- brute force
- math
- number theory

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
3
10 4
12 6
179 822
```

**Output**:
```
10
4
179
```

### Example 2

**Input**:
```
1
42034266112 80174
```

**Output**:
```
1048576
```

### Example 3

**Input**:
```
10
246857872446986130 713202678
857754240051582063 933416507
873935277189052612 530795521
557307185726829409 746530097
173788420792057536 769449696
101626841876448103 132345797
598448092106640578 746411314
733629261048200000 361714100
981271355542147402 38
559754147245184151 431517529
```

**Output**:
```
123428936223493065
918940509
37932865019708
1
57929473597352512
767888699
299224046053320289
31896924393400000
490635677771073701
26946235365387
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
