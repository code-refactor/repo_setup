# 61_E. Enemy is weak

**ID:** 61_e_enemy_is_weak_2240
**Difficulty:** 11

## Description

The Romans have attacked again. This time they are much more than the Persians but Shapur is ready to defeat them. He says: "A lion is never afraid of a hundred sheep". 

Nevertheless Shapur has to find weaknesses in the Roman army to defeat them. So he gives the army a weakness number.

In Shapur's opinion the weakness of an army is equal to the number of triplets i, j, k such that i < j < k and ai > aj > ak where ax is the power of man standing at position x. The Roman army has one special trait — powers of all the people in it are distinct.

Help Shapur find out how weak the Romans are.

Input

The first line of input contains a single number n (3 ≤ n ≤ 106) — the number of men in Roman army. Next line contains n different positive integers ai (1 ≤ i ≤ n, 1 ≤ ai ≤ 109) — powers of men in the Roman army. 

Output

A single integer number, the weakness of the Roman army. 

Please, do not use %lld specificator to read or write 64-bit integers in C++. It is preffered to use cout (also you may use %I64d).

Examples

Input

3
3 2 1


Output

1


Input

3
2 3 1


Output

0


Input

4
10 8 3 1


Output

4


Input

4
1 5 4 3


Output

1

## Categories

- data structures
- trees

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4
1 5 4 3
```

**Output**:
```
1
```

### Example 2

**Input**:
```
3
3 2 1
```

**Output**:
```
1
```

### Example 3

**Input**:
```
3
2 3 1
```

**Output**:
```
0
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
