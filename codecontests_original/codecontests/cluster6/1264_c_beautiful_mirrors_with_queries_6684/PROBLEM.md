# 1264_C. Beautiful Mirrors with queries

**ID:** 1264_c_beautiful_mirrors_with_queries_6684
**Difficulty:** 9

## Description

Creatnx has n mirrors, numbered from 1 to n. Every day, Creatnx asks exactly one mirror "Am I beautiful?". The i-th mirror will tell Creatnx that he is beautiful with probability (p_i)/(100) for all 1 ≤ i ≤ n.

Some mirrors are called checkpoints. Initially, only the 1st mirror is a checkpoint. It remains a checkpoint all the time.

Creatnx asks the mirrors one by one, starting from the 1-st mirror. Every day, if he asks i-th mirror, there are two possibilities:

  * The i-th mirror tells Creatnx that he is beautiful. In this case, if i = n Creatnx will stop and become happy, otherwise he will continue asking the i+1-th mirror next day; 
  * In the other case, Creatnx will feel upset. The next day, Creatnx will start asking from the checkpoint with a maximal number that is less or equal to i. 



There are some changes occur over time: some mirrors become new checkpoints and some mirrors are no longer checkpoints. You are given q queries, each query is represented by an integer u: If the u-th mirror isn't a checkpoint then we set it as a checkpoint. Otherwise, the u-th mirror is no longer a checkpoint.

After each query, you need to calculate [the expected number](https://en.wikipedia.org/wiki/Expected_value) of days until Creatnx becomes happy.

Each of this numbers should be found by modulo 998244353. Formally, let M = 998244353. It can be shown that the answer can be expressed as an irreducible fraction p/q, where p and q are integers and q not ≡ 0 \pmod{M}. Output the integer equal to p ⋅ q^{-1} mod M. In other words, output such an integer x that 0 ≤ x < M and x ⋅ q ≡ p \pmod{M}.

Input

The first line contains two integers n, q (2 ≤ n, q ≤ 2 ⋅ 10^5) — the number of mirrors and queries.

The second line contains n integers: p_1, p_2, …, p_n (1 ≤ p_i ≤ 100).

Each of q following lines contains a single integer u (2 ≤ u ≤ n) — next query.

Output

Print q numbers – the answers after each query by modulo 998244353.

Examples

Input


2 2
50 50
2
2


Output


4
6


Input


5 5
10 20 30 40 50
2
3
4
5
3


Output


117
665496274
332748143
831870317
499122211

Note

In the first test after the first query, the first and the second mirrors are checkpoints. Creatnx will ask the first mirror until it will say that he is beautiful, after that he will ask the second mirror until it will say that he is beautiful because the second mirror is a checkpoint. After that, he will become happy. Probabilities that the mirrors will say, that he is beautiful are equal to 1/2. So, the expected number of days, until one mirror will say, that he is beautiful is equal to 2 and the answer will be equal to 4 = 2 + 2.

## Categories

- data structures
- probabilities

## Source

Codeforces

## Examples

### Example 1

**Input**:
```
2 2
50 50
2
2
```

**Output**:
```
4
6
```

### Example 2

**Input**:
```
5 5
10 20 30 40 50
2
3
4
5
3
```

**Output**:
```
117
665496274
332748143
831870317
499122211
```

### Example 3

**Input**:
```
2 2
38 4
2
2
```

**Output**:
```
262695910
577931032
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
