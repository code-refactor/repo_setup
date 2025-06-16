# 156_D. Clues

**ID:** 156_d_clues_3678
**Difficulty:** 10

## Description

As Sherlock Holmes was investigating another crime, he found a certain number of clues. Also, he has already found direct links between some of those clues. The direct links between the clues are mutual. That is, the direct link between clues A and B and the direct link between clues B and A is the same thing. No more than one direct link can exist between two clues.

Of course Sherlock is able to find direct links between all clues. But it will take too much time and the criminals can use this extra time to hide. To solve the crime, Sherlock needs each clue to be linked to all other clues (maybe not directly, via some other clues). Clues A and B are considered linked either if there is a direct link between them or if there is a direct link between A and some other clue C which is linked to B. 

Sherlock Holmes counted the minimum number of additional direct links that he needs to find to solve the crime. As it turns out, it equals T.

Please count the number of different ways to find exactly T direct links between the clues so that the crime is solved in the end. Two ways to find direct links are considered different if there exist two clues which have a direct link in one way and do not have a direct link in the other way. 

As the number of different ways can turn out rather big, print it modulo k.

Input

The first line contains three space-separated integers n, m, k (1 ≤ n ≤ 105, 0 ≤ m ≤ 105, 1 ≤ k ≤ 109) — the number of clues, the number of direct clue links that Holmes has already found and the divisor for the modulo operation.

Each of next m lines contains two integers a and b (1 ≤ a, b ≤ n, a ≠ b), that represent a direct link between clues. It is guaranteed that any two clues are linked by no more than one direct link. Note that the direct links between the clues are mutual.

Output

Print the single number — the answer to the problem modulo k.

Examples

Input

2 0 1000000000


Output

1


Input

3 0 100


Output

3


Input

4 1 1000000000
1 4


Output

8

Note

The first sample only has two clues and Sherlock hasn't found any direct link between them yet. The only way to solve the crime is to find the link.

The second sample has three clues and Sherlock hasn't found any direct links between them. He has to find two of three possible direct links between clues to solve the crime — there are 3 ways to do it.

The third sample has four clues and the detective has already found one direct link between the first and the fourth clue. There are 8 ways to find two remaining clues to solve the crime.

## Categories

- combinatorics
- graphs

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
4 1 1000000000
1 4
```

**Output**:
```
8
```

### Example 2

**Input**:
```
3 0 100
```

**Output**:
```
3
```

### Example 3

**Input**:
```
2 0 1000000000
```

**Output**:
```
1
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
